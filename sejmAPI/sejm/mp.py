from enum import StrEnum
from datetime import date
from .utils import BASE_URL, parse_normal_date, parse_iso_format
import httpx

class Mp:
    def __init__(self, raw: dict):
        self.accusative_name = raw.get('accusativeName', '')
        self.active = raw.get('active', False)
        self.birth_date = parse_normal_date(raw.get('birthDate', ''), '%Y-%m-%d')
        self.birth_location = raw.get('birthLocation', '')
        self.club = raw.get('club', '')
        self.district_name = raw.get('districtName', '')
        self.district_num = raw.get('districtNum', -1)
        self.education_level = raw.get('educationLevel', '')
        self.email = raw.get('email', '')
        self.first_last_name = raw.get('firstLastName', '')
        self.first_name = raw.get('firstName', '')
        self.genitive_name = raw.get('genitiveName', '')
        self.id = raw.get('id', -1)
        self.inactive_cause = raw.get('inactiveCause', '')
        self.last_first_name = raw.get('lastFirstName', '')
        self.last_name = raw.get('lastName', '')
        self.number_of_votes = raw.get('numberOfVotes', -1)
        self.profession = raw.get('profession', '')
        self.second_name = raw.get('secondName', '')
        self.voivodeship = raw.get('voivodeship', '')

    def build_photo_uri(self, term:int):
        return f'{BASE_URL}/sejm/term{term}/MP/{self.id}/photo'

    def build_mini_photo_uri(self, term:int):
        return f'{BASE_URL}/sejm/term{term}/MP/{self.id}/photo-mini'

    def __str__(self):
        return f'{self.first_last_name} ({self.birth_date}, {self.birth_location}), {self.club}'

    def __repr__(self):
        return f'{self.first_last_name} ({self.birth_date}, {self.birth_location}), {self.club}'

class VoteMP:
    class VoteEnum(StrEnum):
        yes='YES'
        no='NO'
        abstain='ABSTAIN'
        no_vote='NO_VOTE'
        absent='ABSENT'
        vote_valid='VOTE_VALID'
        vote_invalid = 'VOTE_INVALID'

    def __init__(self, raw:dict):
        self.voting_number = raw.get('votingNumber')
        self.date = parse_iso_format(raw.get('date', ''))
        self.title = raw.get('title')
        self.description  = raw.get('description')
        self.topic = raw.get('topic')
        self.kind = raw.get('kind')
        self.vote = raw.get('vote')
        self.list_votes = [VoteMP.VoteEnum(v) for v in raw.get('listVotes', [])] # NOTE: Obiekty zawarte w liście odwołują się do VotingOption w danym głosowaniu

    def __str__(self):
        return f'VoteMP(voting_number={self.voting_number}, title={self.title})'

    def __repr__(self):
        return f'VoteMP(voting_number={self.voting_number}, title={self.title})'

def get_mps(session:httpx.Client, term:int):
    res = session.get(f'{BASE_URL}/sejm/term{term}/MP')
    res.raise_for_status()
    return list(map(lambda d:Mp(d), res.json()))

def get_mp_photo(session:httpx.Client, uri:str):
    """Zdjęcie powinno być pobrane w rozszerzeniu .jfif"""
    res = session.get(uri)
    res.raise_for_status()
    return res.content

def get_mp_vote(session:httpx.Client,term:int,  id:int, sitting:int, date:date):
    """Pobierz informacje o głosowaniu danego posła, danym posiedzeniu o konkretnej dacie"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/MP/{id}/votings/{sitting}/{str(date)}')
    res.raise_for_status()
    return [VoteMP(e) for e in res.json()]

async def async_get_mp_vote(session:httpx.AsyncClient,term:int,  id:int, sitting:int, date:date):
    """Pobierz informacje o głosowaniu danego posła, danym posiedzeniu o konkretnej dacie"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/MP/{id}/votings/{sitting}/{str(date)}')
    res.raise_for_status()
    return [VoteMP(e) for e in res.json()]


async def async_get_mps(session:httpx.AsyncClient, term:int):
    res = await session.get(f'{BASE_URL}/sejm/term{term}/MP')
    res.raise_for_status()
    return list(map(lambda d: Mp(d), res.json()))

async def async_get_mp_photo(session:httpx.AsyncClient, uri:str):
    """Zdjęcie powinno być pobrane w rozszerzeniu .jfif"""
    res = await session.get(uri)
    res.raise_for_status()
    return res.content

__all__ = ['Mp', 'get_mps', 'get_mp_photo', 'async_get_mps', 'async_get_mp_photo', 'VoteMP', 'get_mp_vote', 'async_get_mp_vote']
