"""Moduł oparty o: https://api.sejm.gov.pl/votings.html#lista-glosowan"""
from .utils import BASE_URL, parse_normal_date, parse_iso_format
import datetime
import httpx

class VotingOption:
    def __init__(self, raw:dict):
        self.option_index = raw.get('optionIndex')
        self.option = raw.get('option')
        self.description  = raw.get('description ')
        self.votes = raw.get('votes')

    def __str__(self):
        return f'VotingOption(option={self.option}, votes={self.votes})'

class Vote:
    def __init__(self, raw:dict):
        self.mp = raw.get('mp')
        self.club = raw.get('club')
        self.first_name = raw.get('firstName')
        self.last_name = raw.get('lastName')
        self.vote = raw.get('vote')
        self.list_votes = [VotingOption(v) for v in raw.get('listVotes', [])]

    def __str__(self):
        return f'Vote(mp={self.mp}, vote={self.vote})'

class Voting:
    def __init__(self, raw: dict):
        self.term = raw.get('term')
        self.sitting = raw.get('sitting')
        self.sittingDay = raw.get('sittingDay')
        self.votingNumber = raw.get('votingNumber')
        self.yes = raw.get('yes')
        self.no = raw.get('no')
        self.abstain = raw.get('abstain')
        self.notParticipating = raw.get('notParticipating')
        self.totalVoted = raw.get('totalVoted')
        self.date = parse_iso_format(raw.get('date'))
        self.title = raw.get('title')
        self.description = raw.get('description')
        self.topic = raw.get('topic')
        self.pdfLink = raw.get('pdfLink')
        self.kind = raw.get('kind')
        self.votingOptions = [VotingOption(v) for v in raw.get('listVotes', [])]
        self.votes = [Vote  (v) for v in raw.get('votes', [])]

    def __str__(self):
        return f"Voting {self.votingNumber} - {self.title} on {self.date}"

class VoteMP:
    def __init__(self, raw:dict):
        self.voting_number = raw.get('votingNumber')
        self.date = parse_iso_format(raw.get('date'))
        self.title = raw.get('title')
        self.description  = raw.get('description')
        self.topic = raw.get('topic')
        self.kind = raw.get('kind')
        self.vote = raw.get('vote')
        self.list_votes = raw.get('listVotes', []) # NOTE: Obiekty zawarte w liście odwołują się do VotingOption w danym głosowaniu

    def __str__(self):
        return f'VoteMP(voting_number={self.voting_number}, title={self.title})'


class Sitting:
    def __init__(self, raw:dict):
        self.date = parse_normal_date(raw.get('date'), '%Y-%m-%d')
        self.proceeding = raw.get('proceeding')
        self.votings_num = raw.get('votingsNum')

    def __str__(self):
        return f'Sitting(date={self.date}, proceeding={self.proceeding}, votings_num={self.votings_num})'

def get_voting_list(session:httpx.Client, term:int, sitting:int):
    """Zwraca listę głosowań na danym posiedzeniu Sejmu."""
    res = session.get(f'{BASE_URL}/sejm/term{term}/votings/{sitting}')
    res.raise_for_status()
    return list(map(lambda d:Voting(d), res.json()))

def get_votings(session:httpx.Client, term:int):
    """Zwraca listę posiedzeń dla danej kadencji."""
    res = session.get(f'{BASE_URL}/sejm/term{term}/votings')
    res.raise_for_status()
    return list(map(lambda d:Sitting(d), res.json()))

def get_voting_details(session:httpx.Client, term:int, sitting:int, voting_num:int):
    """Zwraca szczegóły głosowania na danym posiedzeniu Sejmu."""
    res = session.get(f'{BASE_URL}/sejm/term{term}/votings/{sitting}/{voting_num}')
    res.raise_for_status()
    return Voting(res.json())

def get_mp_votings(session:httpx.Client, term:int, mp_id:int, sitting:int, date:datetime.date):
    """Zwraca wyniki głosowania danego posła w dany dzień głosowań.
    :parameter date musi być w formacie yyyy-mm-dd"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/MP/{mp_id}/votings/{sitting}/{date}')
    res.raise_for_status()
    return res.json()

async def async_get_voting_list(session: httpx.AsyncClient, term: int, sitting: int):
    """Zwraca listę głosowań na danym posiedzeniu Sejmu (wersja asynchroniczna)."""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/votings/{sitting}')
    res.raise_for_status()
    return list(map(lambda d: Voting(d), res.json()))

async def async_get_votings(session: httpx.AsyncClient, term: int):
    """Zwraca listę posiedzeń dla danej kadencji (wersja asynchroniczna)."""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/votings')
    res.raise_for_status()
    return list(map(lambda d: Sitting(d), res.json()))

async def async_get_voting_details(session: httpx.AsyncClient, term: int, sitting: int, voting_num: int):
    """Zwraca szczegóły głosowania na danym posiedzeniu Sejmu (wersja asynchroniczna)."""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/votings/{sitting}/{voting_num}')
    res.raise_for_status()
    return Voting(res.json())

async def async_get_mp_votings(session: httpx.AsyncClient, term: int, mp_id: int, sitting: int, date: datetime.date):
    """Zwraca wyniki głosowania danego posła w dany dzień głosowań (wersja asynchroniczna).
    :parameter date musi być w formacie yyyy-mm-dd"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/MP/{mp_id}/votings/{sitting}/{date}')
    res.raise_for_status()
    return res.json()


__all__ = ['VotingOption', 'Vote', 'Voting', 'VoteMP', 'Sitting', 'get_voting_list', 'get_votings', 'get_mp_votings', 'get_voting_details',
           'async_get_voting_list', 'async_get_votings', 'async_get_mp_votings', 'async_get_voting_details']
