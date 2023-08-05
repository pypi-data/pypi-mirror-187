"""
This submodule handles parsing the HTML versions
of the Atlas pages to generate Python models of
the data.
"""
import re

from bs4 import BeautifulSoup # type: ignore
from bs4.element import Tag, PageElement   # type: ignore
import requests
import datetime
import warnings
from moneyed import Money, USD

from .models import *

def parse_search_result(row: Tag) -> Optional[RFPSearchResult]:
    parsed = {}
    for i, col in enumerate(row.find_all('td', class_='data')):
        if i == 0:
            # Should be an a href
            a_tag = col.find('a')
            if a_tag is None:
                warnings.warn('Unable to find RFP details hyperlink')
                return None
            parsed['rfp_number'] = int(a_tag.text)
            parsed['rfp_details_url'] = f'https://adminappsts.mit.edu/rfp/{a_tag["href"]}'
        elif i == 1:
            parsed['creation_date'] = datetime.datetime.strptime(
                col.text.strip(),
                "%m/%d/%Y"
            ).date()
        elif i == 2:
            parsed['payee'] = Person(name=col.text.strip())
        elif i == 3:
            parsed['created_by'] = Person(
                name=col['title'],
                kerberos=col.text.strip()
            )
        elif i == 4:
            parsed['rfp_name'] = col.text.strip()
        elif i == 5:
            # Check if it is payed or not
            if col.text.strip() == 'Paid':
                parsed['location_status'] = 'Paid'
            else:
                parsed['location_status'] = Person(
                    name = col['title'],
                    kerberos=col.find('a').text.strip()
                )
        elif i == 6:
            if col.text.strip() == 'Multiple':
                parsed['cost_object'] = 'Multiple'
            else:
                parsed['cost_object'] = CostObject(
                    id = int(col.text.strip()),
                    name = col['title']
                )
        elif i == 7:
            parsed['amount'] = Money(col.text.strip().strip('$'), USD)
    return RFPSearchResult(**parsed)

# Predicates for searching
def _filter_previous_sibling(tag, func) -> bool:
    previous_tag = tag.find_previous_sibling()
    if previous_tag is None:
        return False
    return func(previous_tag)

def _has_class(tag, class_str) -> bool:
    classes = tag.get('class')
    if classes is None:
        return False
    return class_str in classes

def _data_td_preceded_by_th(tag, th_str) -> bool:
    return (
        tag.name == 'td' and
        _has_class(tag, 'data') and
        _filter_previous_sibling(tag,
            lambda sibling: sibling.name == 'th'
            and sibling.text.strip() == th_str
        )
    )

def _class_preceded_by_tag(tag, tag_class, pre_tag, pre_str) -> bool:
    return (
        _has_class(tag, tag_class) and
        _filter_previous_sibling(tag,
            lambda sibling: sibling.name == pre_tag
            and sibling.text.strip() == pre_str
        )
    )

def parse_rfp_details(response: requests.Response) -> Optional[RFP]:
    page = BeautifulSoup(response.text, features='html.parser')

    rfp = {}

    current_status_div = page.find(
        lambda tag: tag.name == 'div'
        and _filter_previous_sibling(tag,
            lambda sibling: sibling.name == 'h2'
            and sibling.text.strip() == 'Current Status'
        )
    )
    if current_status_div is None:
        warnings.warn('Unable to locate Current Status table')
        return None
    inbox_status = current_status_div.find(
        lambda tag: _data_td_preceded_by_th(tag, 'Status')
    )
    if inbox_status is None:
        warnings.warn('Unable to locate inbox status field!')
        return None
    inbox = inbox_status.text.strip()
    if inbox == 'Sent to bank for payment':
        rfp['inbox'] = 'Paid'

    # Find the section container preceded by the H2 "Payment Details"
    details_div = page.find(
        lambda tag: tag.name == 'div'
        and _filter_previous_sibling(tag,
            lambda sibling: sibling.name == 'h2'
            and sibling.text.strip() == 'Payment Details'
        )
    )
    if details_div is None:
        warnings.warn('Unable to locate Payment Details table in RFP details')
        return None
    
    rfp_number_td = details_div.find(
        lambda tag: _data_td_preceded_by_th(tag, 'RFP Number')
    )
    if rfp_number_td is None:
        warnings.warn('Unable to locate RFP number field in RFP details')
        return None
    rfp['rfp_number'] = int(rfp_number_td.text.strip())

    payee_td = details_div.find(
        lambda tag: _data_td_preceded_by_th(tag, 'Payee')
    )
    if payee_td is None:
        warnings.warn('Unable to locate payee field in RFP details')
        return None
    rfp['payee'] = Person(name=payee_td.text.strip())

    rfp_name_td = details_div.find(
        lambda tag: _data_td_preceded_by_th(tag, 'Name of RFP')
    )
    if rfp_name_td is None:
        warnings.warn('Unable to locate RFP name field in RFP details')
        return None
    rfp['rfp_name'] = rfp_name_td.text.strip()

    # Company code, rfp type, payment method are loaded from the details div
    company_code_td = details_div.find(
        lambda tag: _data_td_preceded_by_th(tag, 'Company Code')
    )
    if company_code_td is None:
        warnings.warn('Unable to locate Company Code entry')
        return None
    rfp['company_code'] = company_code_td.text.strip()

    rfp_type_td = details_div.find(
        lambda tag: _data_td_preceded_by_th(tag, 'Type of RFP')
    )
    if rfp_type_td is None:
        warnings.warn('Unable to locate Type of RFP entry')
        return None
    rfp['rfp_type'] = rfp_type_td.text.strip()

    payment_method_td = details_div.find(
        lambda tag: _data_td_preceded_by_th(tag, 'Payment Method')
    )
    rfp['payment_method'] = payment_method_td.text.strip()

    rfp['line_items'] = []
    for line_item in page.find_all('div', attrs={'class': 'lineItem'}):
        item = {}
        item['approved'] = line_item.find('img', alt='approved') is not None

        details_table = line_item.find('table', attrs={'class': 'topHeadersTable'})
        if details_table is None:
            warnings.warn('Unable to find line-item details table')
            return None
        tbody = details_table.find('tbody')
        if tbody is None:
            warnings.warn('Unable to find line-item table body')
            return None
        
        for i, td in enumerate(tbody.find_all('td', attrs={'class': 'data'})):
            if i == 0:
                item['date_of_service'] = datetime.datetime.strptime(
                    td.text.strip(),
                    "%m/%d/%Y"
                ).date()
            elif i == 1:
                account_match = re.match(r"(?P<id>\d+) - (?P<name>.+)", td.text.strip())
                if account_match is None:
                    warnings.warn('Unable to parse the line item GL account')
                    return None
                item['gl_account'] = GLAccount(
                    id=int(account_match['id']),
                    name=account_match['name']
                )
            elif i == 2:
                co_match = re.match(r"(?P<id>\d+) - (?P<name>.+)", td.text.strip())
                if co_match is None:
                    warnings.warn('Unable to parse the line item cost object')
                    return None
                item['cost_object'] = CostObject(
                    id=int(co_match['id']),
                    name=co_match['name']
                )
            elif i == 3:
                item['amount'] = Money(td.text.strip().strip('$'), USD)
            else:
                warnings.warn(f'Unexpected entry in line item details table! Entry: {td}')
                return None
        # Locate explanation
        explanation_div = line_item.find(
            lambda tag: _class_preceded_by_tag(
                tag, 'data', 'h4', 'Explanation'
        ))
        if explanation_div is None:
            warnings.warn('Unable to locate explanation div in line item!')
            return None
        item['explanation'] = explanation_div.text.strip()
        rfp['line_items'].append(LineItem(**item))
    
    rfp['amount'] = sum([item.amount for item in rfp['line_items']])
    # Load office note
    office_note_div = page.find(
        lambda tag: _class_preceded_by_tag(
            tag, 'sectionContainer', 'h3', 'Note to Central Office'
        )
    )
    if office_note_div is None:
        warnings.warn('Unable to locate Note to Central Office div')
        return None
    rfp['office_note'] = office_note_div.find('div', attrs={'class': 'data'}).text.strip()

    receipts_div = page.find('div', attrs={'class': 'receiptsList'})
    if receipts_div is None:
        warnings.warn('Unable to locate receipt list')
        return None
    rfp['receipts'] = []
    for tag in receipts_div.find_all('a'):
        rfp['receipts'].append(Receipt(
            id=re.match(r'#(\d+),?', tag.text.strip()).group(1),
            url=f"https://adminappsts.mit.edu{tag['href']}"
        ))
    
    history_div = page.find(
        lambda tag: _class_preceded_by_tag(
            tag, 'sectionContainer', 'h2', 'RFP History'
        )
    )
    if history_div is None:
        warnings.warn('Unable to locate history div')
        return None
    rfp['history'] = []
    history_table = history_div.find('tbody')
    if history_table is None:
        warnings.warn('Unable to locate the history table')
        return None
    
    for row in history_table.find_all('tr'):
        cells = list(row.find_all('td', attrs={'class': 'data'}))
        if len(cells) < 3:
            warnings.warn('Unable to parse history row')
            return None
        rfp['history'].append(RFPAction(
            datetime=datetime.datetime.strptime(
                f'{cells[0].text.strip()} {cells[1].text.strip()}',
                "%m/%d/%Y %I:%M %p"
            ),
            action=cells[2].text.strip()
        ))
    return RFP(**rfp)
    

def parse_search(search_response:requests.Response) -> List[RFPSearchResult]:
    """
    Parses a Response object into a list of RFP search results.

    Arguments
    ---------
    search_response: A HTML response containing the Atlas RFP search page.

    Returns
    -------
    A list of RFPSearchResults representing the search results.
    """
    html = BeautifulSoup(search_response.text, features='html.parser')
    # Get the search results table
    results_table = html.find(id='searchResultsTable')
    if results_table is None:
        raise RuntimeError('Unable to find search results table!')
    results_body = results_table.find('tbody')
    if not isinstance(results_body, Tag):
        raise RuntimeError('Unable to locate `tbody` tag in search results table!')
    return [x for x in 
           [parse_search_result(row) for row in results_body.find_all('tr')]
           if x is not None]
