"""
Helper Pydantic models that define the state
of the RFP system. We can load these models
using Beautifulsoup for parsing.
"""
import datetime
from typing import List, Optional, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from pydantic import BaseModel, PositiveInt, HttpUrl
from moneyed import Money

class Person(BaseModel):
    """
    Model representing a person.

    The name field is required, the
    kerberos is optional (not displayed
    in several RFP pages).
    """
    name: str
    kerberos: Optional[str]

class MailingInstructions(BaseModel):
    """
    Model representing extra mailing
    instructions.
    Used for non-direct-deposit reimbursements.
    """
    addressee: Person
    phone: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str
    tax_type: str
    ssn_tin: str

class GLAccount(BaseModel):
    """
    A model representing a
    GL account, separating its
    ID and name.
    """
    id: int
    name: str

class CostObject(BaseModel):
    """
    A model representing a
    cost object, separating its
    ID and name.
    """
    id: int
    name: str

class LineItem(BaseModel):
    """
    A model defining a reimbursable
    line-item.
    """
    approved: bool
    date_of_service: datetime.date
    gl_account: GLAccount
    cost_object: CostObject
    amount: Money
    explanation: str

    # Allow the Money entry
    class Config:
        arbitrary_types_allowed = True

class Receipt(BaseModel):
    id: PositiveInt
    url: HttpUrl

class RFPAction(BaseModel):
    """
    A model representing an action taken on an RFP.
    """
    datetime: datetime.datetime
    action: str

class RFP(BaseModel):
    """
    A model representing a submitted RFP.
    """
    inbox: Union[Person,Literal['Paid']]
    rfp_number: PositiveInt
    payee: Person
    company_code: str
    rfp_name: str
    rfp_type: str
    amount: Money
    payment_method: Union[MailingInstructions,Literal['Direct Deposit']]
    line_items: List[LineItem]
    office_note: str
    receipts: List[Receipt]
    history: List[RFPAction]
    # Allow the Money entry
    class Config:
        arbitrary_types_allowed = True

class RFPSearchResult(BaseModel):
    """
    A model representing a RFP search result.

    In addition to some basic information about
    the RFP, this object also includes the URL
    needed to get RFP details.
    """
    rfp_number: PositiveInt
    rfp_details_url: HttpUrl
    creation_date: datetime.date
    payee: Person
    created_by: Person
    rfp_name: str
    location_status: Union[Person,Literal['Paid']]
    cost_object: Union[CostObject,Literal['Multiple']]
    amount: Money
    # Allow the Money entry
    class Config:
        arbitrary_types_allowed = True