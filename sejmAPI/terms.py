"""Moduł oparty o: https://api.sejm.gov.pl/term.html"""
from .exceptions import invalidLinkException
from .utils import BASE_URL, parse_iso_format, parse_normal_date
import httpx

class Prints:
    def __init__(self, raw:dict):
        self.raw = raw

    @property
    def count(self):
        return self.raw['count']

    @property
    def last_changed(self):
        return parse_iso_format(self.raw['lastChanged'])

    @property
    def link(self):
        if type(self.raw['link'] is bool):
            raise invalidLinkException("Invalid term's print link")
        return self.raw['link']


    def build_uri(self):
        return f'{BASE_URL}/sejm{self.link}'


class Term:
    def __init__(self, raw:dict):
        self.raw = raw
        self.to = raw.get('to', None)

    @property
    def current(self):
        return self.raw['current']

    @property
    def start(self):
        return parse_normal_date(self.raw['from'], '%Y-%m-%d').date()

    @property
    def num(self):
        return self.raw['num']

    @property
    def prints(self):
        return Prints(self.raw['prints'])

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



