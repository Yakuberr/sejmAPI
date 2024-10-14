from utils import BASE_URL, filter_query_params, parse_normal_date, parse_iso_format
from datetime import date, datetime
from urllib.parse import urlencode
from enum import StrEnum
import httpx

class InterpellationsSortFields(StrEnum):
    NUM = 'num'
    LAST_MODIFIED = 'lastModified '
    RECEIPT_DATE = 'receiptDate '
    SENT_DATE = 'sentDate '

class Link:
    def __init__(self, raw: dict):
        self.href = raw.get('href', '')  # Zmieniamy na 'href' zamiast 'url'
        self.rel = raw.get('rel', '')    # Zmieniamy na 'rel', zgodnie z danymi

    def __repr__(self):
        return f"Link(href='{self.href}', rel='{self.rel}')"

class Attachment:
    def __init__(self, raw: dict):
        self.url = raw.get('URL', '')  # Adres załącznika do pobrania
        self.name = raw.get('name', '')  # Nazwa pliku
        self.last_modified = parse_iso_format(raw.get('lastModified', ''))

    def __str__(self):
        return f'Attachment(url={self.url}, name={self.name})'

class Reply:
    def __init__(self, raw: dict):
        self.key = raw.get('key', '')  # Unikalny identyfikator odpowiedzi
        self.from_ = raw.get('from', '')  # Stanowisko i nazwisko osoby odpowiadającej
        self.links = [Link(link) for link in raw.get('links', [])]  # Lista URLi do treści odpowiedzi
        self.receipt_date = parse_normal_date(raw.get('receiptDate', ''), '%Y-%m-%d')
        self.only_attachment = raw.get('onlyAttachment', False)  # Flaga, czy odpowiedź to tylko załącznik
        self.attachments = [Attachment(att) for att in raw.get('attachments', [])]  # Lista załączników
        self.last_modified = parse_iso_format(raw.get('lastModified', ''))

    def __str__(self):
        return f'Reply(from={self.from_})'

class Interpellation:
    def __init__(self, raw: dict):
        self.term = raw.get('term', 0)
        self.num = raw.get('num', 0)
        self.title = raw.get('title', '')
        self.from_ = raw.get('from', [])  # "from" to słowo kluczowe, więc zmieniamy na "from_"
        self.to = raw.get('to', [])
        self.receipt_date = parse_normal_date(raw.get('receiptDate', ''), '%Y-%m-%d')
        self.sent_date = parse_normal_date(raw.get('sentDate', ''), '%Y-%m-%d')
        self.replies = [Reply(reply) for reply in raw.get('replies', [])]
        self.last_modified = parse_iso_format(raw.get('lastModified', ''))
        self.links = [Link(link) for link in raw.get('links', [])]

    def __str__(self):
        return f'Interpellation(term={self.term}, num={self.num}, title={self.title})'

def get_interpellations(session:httpx.Client, term:int, offset:int=None, limit:int=25, title:str=None, from_mp:str|int=None, to:str=None, since:date=None,
    till:date=None, modifiedSince:datetime=None, sort_by:str|InterpellationsSortFields='', descending=False):
    DESCENDING_MAP = {
        True:'-',
        False:''
    }
    params = {}
    if sort_by != '':
        params['sort_by'] = f'{DESCENDING_MAP[descending]}{sort_by}'
    params = filter_query_params(offset=offset, limit=limit, title=title, from_mp=from_mp, to=to, since=since, till=till, modifiedSince=modifiedSince.strftime('%Y-%m-%dT%H:%M'))
    res = session.get(f'{BASE_URL}/sejm/term{term}/interpellations?' + urlencode(params, safe=':'))
    res.raise_for_status()
    return list(map(lambda d:Interpellation(d), res.json()))


async def async_get_interpellations(session: httpx.AsyncClient, term: int, offset: int = None, limit: int = 25,
                              title: str = None, from_mp: str | int = None, to: str = None, since: date = None,
                              till: date = None, modifiedSince: datetime = None,
                              sort_by: str | InterpellationsSortFields = '', descending=False):
    DESCENDING_MAP = {
        True: '-',
        False: ''
    }
    params = {}
    if sort_by != '':
        params['sort_by'] = f'{DESCENDING_MAP[descending]}{sort_by}'
    params = filter_query_params(
        offset=offset,
        limit=limit,
        title=title,
        from_mp=from_mp,
        to=to,
        since=since,
        till=till,
        modifiedSince=modifiedSince.strftime('%Y-%m-%dT%H:%M') if modifiedSince else None
    )
    res = await session.get(f'{BASE_URL}/sejm/term{term}/interpellations?' + urlencode(params, safe=':'))
    res.raise_for_status()
    return list(map(lambda d: Interpellation(d), res.json()))

__all__ = ['InterpellationsSortFields', 'Link', 'Attachment', 'Reply', 'Interpellation', 'get_interpellations', 'async_get_interpellations']