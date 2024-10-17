"""Moduł oparty o: https://api.sejm.gov.pl/term.html"""
from .exceptions import invalidLinkException
from .utils import BASE_URL, parse_iso_format, parse_normal_date
import httpx

class Prints:
    def __init__(self, raw:dict):
        self.count = raw.get('count')
        self.last_changed = parse_iso_format(raw.get('lastChanged'))
        self.link = raw.get('link')

    def build_uri(self):
        return f'{BASE_URL}/sejm{self.link}'


class Term:
    def __init__(self, raw:dict):
        self.raw = raw
        self.to = raw.get('to', None)
        self.current = raw.get('current')
        self.start = parse_normal_date(raw.get('from'), '%Y-%m-%d')
        self.num = raw.get('num')
        self.prints = Prints(raw.get('prints'))

    def __str__(self):
        return f'<{self.num}, {self.start}>'

def get_current_term(client:httpx.Client):
    try:
        return Term(client.get(f'{BASE_URL}/sejm/term').json()[-1])
    except httpx.RequestError as exc:
        print(f'Error occurred while requesting data: {exc}')
    except KeyError as exc:
        print(f'Invalid response structure: {exc}')


def get_term(client:httpx.Client, term:int):
    res = client.get(f'{BASE_URL}/sejm/term{term}')
    res.raise_for_status()
    return Term(res.json())

async def async_get_current_term(client:httpx.AsyncClient):
    try:
        res = await client.get(f'{BASE_URL}/sejm/term')
    except httpx.RequestError as exc:
        print(f'Error occurred while requesting data: {exc}')
        return
    try:
        t = Term(res.json()[-1])
        return t
    except KeyError as exc:
        print(f'Invalid response structure: {exc}')

async def async_get_term(client:httpx.AsyncClient, term:int):
    res = await client.get(f'{BASE_URL}/sejm/term{term}')
    res.raise_for_status()
    return Term(res.json())

__all__ = ['Prints', 'Term', 'get_current_term', 'get_term', 'async_get_term', 'async_get_current_term']



