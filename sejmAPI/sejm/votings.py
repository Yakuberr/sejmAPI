from enum import StrEnum
from .utils import BASE_URL, parse_normal_date, parse_iso_format, filter_query_params
from datetime import date
import httpx

class VotingOption:
    def __init__(self, raw:dict):
        self.option_index = raw.get('optionIndex', -1)
        self.option = raw.get('option', '')
        self.description  = raw.get('description', '')
        self.votes = raw.get('votes', -1)

    def __str__(self):
        return f'VotingOption(option={self.option}, votes={self.votes})'

class Vote:
    class VoteValueEnum(StrEnum):
        yes="YES"
        no='NO'
        abstain="ABSTAIN"
        no_vote='NO_VOTE'
        absent="ABSENT"
        vote_valid="VOTE_VALID"
        vote_invalid = "VOTE_INVALID"

    def __init__(self, raw:dict):
        self.mp = raw.get('MP', -1)
        self.mP = raw.get('mP', -1)
        self.club = raw.get('club', '')
        self.first_name = raw.get('firstName', '')
        self.last_name = raw.get('lastName', '')
        self.vote = Vote.VoteValueEnum(raw.get('vote'))
        self.list_votes = {k:Vote.VoteValueEnum(v) for k, v in raw.get('listVotes', {})}

    def __str__(self):
        return f'Vote(mp={self.mp}, vote={self.vote})'

class Voting:
    class VotingKindEnum(StrEnum):
        electronic="ELECTRONIC"
        traditional='TRADITIONAL'
        on_list='ON_LIST'

    def __init__(self, raw: dict):
        self.term = raw.get('term', -1)
        self.sitting = raw.get('sitting', -1)
        self.sittingDay = raw.get('sittingDay', -1)
        self.votingNumber = raw.get('votingNumber', -1)
        self.yes = raw.get('yes', -1)
        self.no = raw.get('no', -1)
        self.abstain = raw.get('abstain', -1)
        self.notParticipating = raw.get('notParticipating', -1)
        self.totalVoted = raw.get('totalVoted', -1)
        self.date = parse_iso_format(raw.get('date', ''))
        self.title = raw.get('title', '')
        self.description = raw.get('description', '')
        self.topic = raw.get('topic', '')
        self.pdfLink = raw.get('pdfLink', '')
        self.kind = raw.get('kind')
        self.votingOptions = [VotingOption(v) for v in raw.get('listVotes', [])]
        self.votes = [Vote(v) for v in raw.get('votes', [])]

    def __str__(self):
        return f"Voting {self.votingNumber} - {self.title} on {self.date}"


class Sitting:
    def __init__(self, raw:dict):
        self.date = parse_normal_date(raw.get('date'), '%Y-%m-%d')
        self.proceeding = raw.get('proceeding')
        self.votings_num = raw.get('votingsNum')

    def __str__(self):
        return f'Sitting(date={self.date}, proceeding={self.proceeding}, votings_num={self.votings_num})'

class VotingDetails:
    def __init__(self, raw:dict):
        self.term = raw.get('term', -1)
        self.sitting = raw.get('sitting', -1)
        self.sittingDay = raw.get('sittingDay', -1)
        self.votingNumber = raw.get('votingNumber', -1)
        self.yes = raw.get('yes', -1)
        self.no = raw.get('no', -1)
        self.abstain = raw.get('abstain', -1)
        self.notParticipating = raw.get('notParticipating', -1)
        self.totalVoted = raw.get('totalVoted', -1)
        self.date = parse_iso_format(raw.get('date', ''))
        self.title = raw.get('title', '')
        self.description = raw.get('description', '')
        self.topic = raw.get('topic', '')
        self.pdfLink = raw.get('pdfLink', '')
        self.kind = raw.get('kind')
        self.votingOptions = [VotingOption(v) for v in raw.get('listVotes', [])]
        self.votes = [Vote(v) for v in raw.get('votes', [])]

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

def get_voting_search(session:httpx.Client, term:int, dateFrom:date=None, dateTo:date=None,proceeding:int=None, title:str=None):
    """Zwraca głosowania, które spełniają dane kryteria
    UWAGA: Parametry offset oraz limit sprawiają, że jest zwracany 403
    UWAGA: W przypadku za dużej ilości parametrów zostaje zwracany 403"""
    params = filter_query_params(dateFrom=dateFrom, dateTo=dateTo, proceeding=proceeding, title=title)
    res = session.get(f'{BASE_URL}/sejm/term{term}/votings/search', params=params, headers = {
    "accept": "application/json"
})
    res.raise_for_status()
    return [Voting(v) for v in res.json()]

async def async_get_voting_search(session:httpx.AsyncClient, term:int, dateFrom:date=None, dateTo:date=None,proceeding:int=None, title:str=None):
    """Zwraca głosowania, które spełniają dane kryteria
    UWAGA: Parametry offset oraz limit sprawiają, że jest zwracany 403
    UWAGA: W przypadku za dużej ilości parametrów zostaje zwracany 403"""
    params = filter_query_params(dateFrom=dateFrom, dateTo=dateTo, proceeding=proceeding, title=title)
    res = await session.get(f'{BASE_URL}/sejm/term{term}/votings/search', params=params, headers = {
    "accept": "application/json"
})
    res.raise_for_status()
    return [Voting(v) for v in res.json()]

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


__all__ = ['VotingOption', 'Vote', 'Voting', 'Sitting', 'get_voting_list', 'get_votings', 'get_voting_details',
           'async_get_voting_list', 'async_get_votings', 'async_get_voting_details', 'VotingDetails', 'get_voting_search', 'async_get_voting_search']
