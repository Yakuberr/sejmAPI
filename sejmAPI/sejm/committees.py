from .utils import BASE_URL, parse_normal_date
from enum import StrEnum
import httpx

class Member:
    def __init__(self, raw: dict):
        self.club = raw.get('club', '')
        self.function = raw.get('function', '')  # Niektórzy członkowie mogą nie mieć funkcji
        self.id = raw.get('id', -1)
        self.last_first_name = raw.get('lastFirstName', '')

    def __str__(self):
        return f'{self.last_first_name} ({self.club}, {self.function})'

    def __repr__(self):
        return f'{self.last_first_name} ({self.club}, {self.function})'


class Committee:
    class CommitteeTypeEnum(StrEnum):
        standing = 'STANDING'
        extraordinary = 'EXTRAORDINARY'
        investigative = 'INVESTIGATIVE '

    def __init__(self, raw: dict):
        self.appointment_date = parse_normal_date(raw.get('appointmentDate', ''), '%Y-%m-%d')
        self.code = raw.get('code', '')
        self.composition_date = parse_normal_date(raw.get('compositionDate', ''), '%Y-%m-%d')
        self.members = [Member(member_data) for member_data in raw.get('members')]
        self.name = raw.get('name')
        self.name_genitive = raw.get('nameGenitive')
        self.phone = raw.get('phone', '')
        self.scope = raw.get('scope', '')
        self.type = Committee.CommitteeTypeEnum(raw.get('type'))

    def build_sittings_uri(self, term:int):
        return f'{BASE_URL}/sejm/term{term}/committees/{self.code}/sittings'

    def __str__(self):
        return (f'Committee: {self.name} ({self.code})'
                f'Appointed on: {self.appointment_date}'
                f'Phone: {self.phone}'
                f'Scope: {self.scope}')



class Sitting:
    def __init__(self, raw: dict):
        self.agenda = raw.get('agenda', '').encode('utf-8').decode('unicode_escape')
        self.closed = raw.get('closed', False)
        self.date = parse_normal_date(raw.get('date', ''), '%Y-%m-%d')
        self.joint_with = raw.get('jointWith', [])
        self.num = raw.get('num', -1)
        self.remote = raw.get('remote', False)
        self.video = raw.get('video', [])
        self.audio = raw.get('audio', [])
        self.city = raw.get('city', '')

    def __str__(self):
        return (f'Meeting #{self.num} - {self.date}\n'
                f'Agenda: {self.agenda}\n'
                f'Closed: {"Yes" if self.closed else "No"}\n'
                f'Remote: {"Yes" if self.remote else "No"}\n')

def get_committees(session:httpx.Client, term:int):
    """Zwraca listę komitetów"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/committees')
    res.raise_for_status()
    return list(map(lambda d:Committee(d), res.json()))

def get_committee(session:httpx.Client, term:int, code:str):
    """Zwraca szczegóły komitetu"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/committees/{code}')
    res.raise_for_status()
    return Committee(res.json())

def get_sittings(session:httpx.Client, uri:str):
    """Zwraca listę posiedzeń"""
    res = session.get(uri)
    res.raise_for_status()
    return list(map(lambda d:Sitting(d), res.json()))

def get_sitting(session:httpx.Client, uri:str):
    """Zwraca szczegóły posiedzenia"""
    res = session.get(uri)
    res.raise_for_status()
    return Sitting(res.json())

def get_sitting_transcript(session:httpx.Client, term:int, code:str, num:int, format:str):
    """Zwraca transkrypt dla danego posiedzenia w wybranym formacie: pdf lub html"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/committees/{code}/sittings/{num}/{format}')
    res.raise_for_status()
    if format == 'html':
        return res.text
    return res.content

async def async_get_committees(session:httpx.AsyncClient, term:int):
    """Zwraca listę komitetów"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/committees')
    res.raise_for_status()
    return [Committee(d) for d in res.json()]

async def async_get_committee(session:httpx.AsyncClient, term:int, code:str):
    """Zwraca szczegóły komitetu"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/committees/{code}')
    res.raise_for_status()
    return Committee(res.json())

async def async_get_sittings(session:httpx.AsyncClient, uri:str):
    """Zwraca listę posiedzeń"""
    res = await session.get(uri)
    res.raise_for_status()
    return [Sitting(d) for d in res.json()]

async def async_get_sitting(session:httpx.AsyncClient, uri:str):
    """Zwraca szczegóły posiedzenia"""
    res = await session.get(uri)
    res.raise_for_status()
    return Sitting(res.json())

async def async_get_sitting_transcript(session:httpx.AsyncClient, term:int, code:str, num:int, format:str):
    """Zwraca transkrypt dla danego posiedzenia w wybranym formacie: pdf lub html"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/committees/{code}/sittings/{num}/{format}')
    res.raise_for_status()
    if format == 'html':
        return res.text
    return res.content

__all__ = ['Member', 'Committee', 'Sitting', 'get_committees', 'get_committee', 'get_sittings', 'get_sitting',
           'async_get_sitting', 'async_get_sittings', 'async_get_committee', 'async_get_committees', 'get_sitting_transcript', 'async_get_sitting_transcript']