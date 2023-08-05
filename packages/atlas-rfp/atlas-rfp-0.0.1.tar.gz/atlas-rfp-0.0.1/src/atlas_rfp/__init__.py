from touchstone_auth import TouchstoneSession
from .atlas_parsing import parse_search, parse_rfp_details
from .models import RFP

def search(session:TouchstoneSession, *, rfp_number:int) -> RFP:
    response = session.post(
        'https://adminappsts.mit.edu/rfp/SearchForRfps.action',
        data={
            'taxable': '',
            'criteria.parked': 'true',
            '__checkbox_criteria.parked': 'true',
            'criteria.posted': 'true',
            '__checkbox_criteria.posted': 'true',
            '__checkbox_criteria.deleted': 'true',
            'criteria.companyCode': 'CUR',
            'criteria.rfpNumber': str(rfp_number),
            'criteria.createdDateFrom':'', #MM/DD/YY
            'criteria.createdDateTo': '',
            'criteria.payeeName': '',
            'criteria.shortDescription': '',
            'criteria.costObjectNumber': '',
            'criteria.glAccountNumber': ''
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    )
    return parse_rfp_details(response)