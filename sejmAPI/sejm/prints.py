import httpx
from urllib.parse import quote, unquote
from enum import StrEnum
from .utils import BASE_URL, parse_normal_date, parse_iso_format

class PrintsFieldsEnum(StrEnum):
    NUMBER = 'number'
    DELIVERY_DATE = 'deliveryDate'
    TITLE = 'title'
    TERM = 'term'
    CHANGE_DATE = 'changeDate'
    ATTACHMENTS = 'attachments'

class Print:
    def __init__(self, raw):
        self.number = raw.get('number', '')
        self.delivery_date = parse_normal_date(raw.get('deliveryDate', ''), '%Y-%m-%d')
        self.title = raw.get('title', '')
        self.term = raw.get('term', -1)
        self.change_date = parse_iso_format(raw.get('changeDate', ''))
        self.document_date = parse_normal_date(raw.get('documentDate', ''), '%Y-%m-%d')
        self.attachments = raw.get('attachments', [])
        self.additional_prints = [AdditionalPrint(a) for a in raw.get('additionalPrints',[])]

    def build_uri_attachments(self):
        return [f'{BASE_URL}/sejm/term{self.term}/prints/{self.number}/{quote(a)}' for a in self.attachments]

    def __str__(self):
        return f'<Print {self.number}, {self.delivery_date}, {self.title}>'

class AdditionalPrint(Print):
    def __init__(self, raw):
        super().__init__(raw)
        self.number_associated = raw.get('numberAssociated', '')

class PrintAttachment:
    def __init__(self, file_name, content):
        self.file_name = file_name
        self.content = content

    def save(self, directory="."):
        path = f"{directory}/{self.file_name}"
        with open(path, 'wb') as file:
            file.write(self.content)
        return path


def get_prints(session:httpx.Client, term:int, sort_by:str|PrintsFieldsEnum='', descending=False):
    """Zwraca listę druków"""
    DESCENDING_MAP = {
        True:'-',
        False:''
    }
    sort_query = ''
    if sort_by != '':
        sort_query = f'?sort_by={DESCENDING_MAP[descending]}{sort_by}'
    print(sort_query)
    response = session.get(f'{BASE_URL}/sejm/term{term}/prints{sort_query}')
    response.raise_for_status()
    return [Print(print_data) for print_data in response.json()]


def get_print_details(session:httpx.Client, term:int, print_number):
    """Zwraca szczegóły druku"""
    response = session.get(f'{BASE_URL}/sejm/term{term}/prints/{print_number}')
    response.raise_for_status()
    return Print(response.json())


def get_print_attachment(session:httpx.Client, full_url:str):
    """Zwraca zawartość załącznika druku"""
    response = session.get(full_url)
    response.raise_for_status()
    return PrintAttachment(unquote(full_url.split('/')[7]), response.content)


# Asynchroniczne wersje funkcji
async def async_get_prints(session:httpx.AsyncClient, term:int, sort_by:str|PrintsFieldsEnum='', descending=False):
    """Zwraca listę druków"""
    DESCENDING_MAP = {
        True: '-',
        False: ''
    }
    sort_query = ''
    if sort_by != '':
        sort_query = f'?sort_by={DESCENDING_MAP[descending]}{sort_by}'
    print(sort_query)
    response = await session.get(f'{BASE_URL}/sejm/term{term}/prints{sort_query}')
    response.raise_for_status()
    return [Print(print_data) for print_data in response.json()]


async def async_get_print_details(session:httpx.AsyncClient, term:int, print_number):
    """Zwraca szczegóły druku"""
    response = await session.get(f'{BASE_URL}/sejm/term{term}/prints/{print_number}')
    response.raise_for_status()
    return Print(response.json())


async def async_get_print_attachment(session:httpx.AsyncClient, full_url:str):
    """Zwraca zawartość załącznika druku"""
    response = await session.get(full_url)
    response.raise_for_status()
    print(full_url)
    return PrintAttachment(unquote(full_url.split('/')[7]), response.content)

__all__ = ['PrintsFieldsEnum', 'Print', 'AdditionalPrint', 'PrintAttachment', 'get_prints', 'get_print_details',
           'get_print_attachment', 'async_get_prints', 'async_get_print_details', 'async_get_print_attachment']

