from utils import BASE_URL, parse_normal_date
from enum import StrEnum
import httpx

class Member:
    def __init__(self, raw: dict):
        self.club = raw['club']
        self.function = raw.get('function', '')  # Niektórzy członkowie mogą nie mieć funkcji
        self.id = raw['id']
        self.last_first_name = raw['lastFirstName']

    def __str__(self):
        return f'{self.last_first_name} ({self.club}, {self.function})'


class Committee:
    def __init__(self, raw: dict):
        self.appointment_date = parse_normal_date(raw['appointmentDate'], '%Y-%m-%d').date()
        self.code = raw['code']
        self.composition_date = parse_normal_date(raw['compositionDate'], '%Y-%m-%d').date()
        self.members = [Member(member_data) for member_data in raw['members']]
        self.name = raw['name']
        self.name_genitive = raw['nameGenitive']
        self.phone = raw.get('phone', '')
        self.scope = raw.get('scope', '')
        self.type = raw['type']

    def build_sittings_uri(self, term:int):
        return f'{BASE_URL}/sejm/term{term}/committees/{self.code}/sittings'

    def __str__(self):
        return (f'Committee: {self.name} ({self.code})\n'
                f'Appointed on: {self.appointment_date}\n'
                f'Phone: {self.phone}\n'
                f'Scope: {self.scope}')

class SittingOutputFormat(StrEnum):
        HTML = '/html'
        PDF = '/pdf'
        DEFAULT = ''  # Empty string as an option


class Sitting:
    def __init__(self, raw: dict):
        self.agenda = raw['agenda'].encode('utf-8').decode('unicode_escape')
        self.closed = raw['closed']
        self.date = parse_normal_date(raw['date'], '%Y-%m-%d').date()
        self.joint_with = raw.get('jointWith', [])
        self.num = raw['num']
        self.remote = raw['remote']
        self.video = raw.get('video', [])

    def build_sitting_uri(self, term:int, code:str, output:SittingOutputFormat):
        return f'{BASE_URL}/sejm/term{term}/committees/{code}/sittings/{self.num}{output}'

    def __str__(self):
        return (f'Meeting #{self.num} - {self.date}\n'
                f'Agenda: {self.agenda}\n'
                f'Closed: {"Yes" if self.closed else "No"}\n'
                f'Remote: {"Yes" if self.remote else "No"}\n')

def get_committees(session:httpx.Client, term:int):
    res = session.get(f'{BASE_URL}/sejm/term{term}/committees')
    res.raise_for_status()
    return list(map(lambda d:Committee(d), res.json()))

def get_committee(session:httpx.Client, term:int, code:str):
    res = session.get(f'{BASE_URL}/sejm/term{term}/committees/{code}')
    res.raise_for_status()
    return Committee(res.json())

def get_sittings(session:httpx.Client, uri:str):
    res = session.get(uri)
    res.raise_for_status()
    return list(map(lambda d:Sitting(d), res.json()))

def get_sitting(session:httpx.Client, uri:str):
    res = session.get(uri)
    res.raise_for_status()
    return Sitting(res.json())

async def async_get_committees(session:httpx.AsyncClient, term:int):
    res = await session.get(f'{BASE_URL}/sejm/term{term}/committees')
    res.raise_for_status()
    return [Committee(d) for d in res.json()]

async def async_get_committee(session:httpx.AsyncClient, term:int, code:str):
    res = await session.get(f'{BASE_URL}/sejm/term{term}/committees/{code}')
    res.raise_for_status()
    return Committee(res.json())

async def async_get_sittings(session:httpx.AsyncClient, uri:str):
    res = await session.get(uri)
    res.raise_for_status()
    return [Sitting(d) for d in res.json()]

async def async_get_sitting(session:httpx.AsyncClient, uri:str):
    res = await session.get(uri)
    res.raise_for_status()
    return Sitting(res.json())

__all__ = ['Member', 'Committee', 'SittingOutputFormat', 'Sitting', 'get_committees', 'get_committee', 'get_sittings', 'get_sitting',
           'async_get_sitting', 'async_get_sittings', 'async_get_committee', 'async_get_committees']