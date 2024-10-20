from .utils import BASE_URL, parse_normal_date, parse_iso_format
from datetime import date
import httpx

class Proceeding:
    def __init__(self, raw:dict):
        self.title = raw.get('title', '')
        self.dates = list(map(lambda d:parse_normal_date(d, format='%Y-%m-%d'), raw.get('dates', [])))
        self.number = raw.get('number', 0)

    def __str__(self):
        return f'Proceeding(title={self.title}, number={self.number})'

class Statement:
    def __init__(self, raw:dict):
        self.num = raw.get('num', -1)
        self.function = raw.get('function', '')
        self.name = raw.get('name', '')
        self.member_id = raw.get('memberID', -1)
        self.rapporteur = raw.get('rapporteur', False)
        self.secretary = raw.get('secretary', False)
        self.unspoken = raw.get('unspoken', False)
        self.start_datetime = parse_iso_format(raw.get('startDateTime', ''))
        self.end_datetime = parse_iso_format(raw.get('endDateTime', ''))

    def __str__(self):
        return f'Statement(num={self.num}, function={self.function})'

class StatementList:
    def __init__(self, raw:dict):
        self.proceeding_num = raw.get('proceedingNum', -1)
        self.date = parse_normal_date(raw.get('date', ''), '%Y-%m-%d')
        self.statements = [Statement(s) for s in raw.get('statements', [])]

    def __str__(self):
        return f'StatementList(proceeding_num={self.proceeding_num}, date={self.date})'

def get_proceedings(session:httpx.Client, term:int):
    """Zwraca listę posiedzeń"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/proceedings')
    res.raise_for_status()
    return list(map(lambda d:Proceeding(d), res.json()))

def get_proceeding(session:httpx.Client, term:int, p_id:int):
    """Zwraca informacje o danym posiedzeniu"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/proceedings/{p_id}')
    res.raise_for_status()
    return Proceeding(res.json())

async def async_get_proceedings(session: httpx.AsyncClient, term: int):
    """Asynchroniczna funkcja zwracająca listę posiedzeń"""
    url = f'{BASE_URL}/sejm/term{term}/proceedings'
    res = await session.get(url)
    res.raise_for_status()
    return [Proceeding(d) for d in res.json()]

async def async_get_proceeding(session: httpx.AsyncClient, term: int, p_id: int):
    """Asynchroniczna funkcja zwracająca informacje o danym posiedzeniu"""
    url = f'{BASE_URL}/sejm/term{term}/proceedings/{p_id}'
    res = await session.get(url)
    res.raise_for_status()
    return Proceeding(res.json())

def get_transcript(session:httpx.Client, term:int, id:int, d:date):
    """Zwróć oświadczenia dla danego posiedzenia w danym dniu"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/proceedings/{id}/{d}/transcripts')
    res.raise_for_status()
    return StatementList(res.json())

async def async_get_transcript(session:httpx.AsyncClient, term:int, id:int, d:date):
    """Zwróć oświadczenia dla danego posiedzenia w danym dniu"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/proceedings/{id}/{d}/transcripts')
    res.raise_for_status()
    return StatementList(res.json())

def get_transcript_pdf(session:httpx.Client, term:int, id:int, d:date):
    """Zwróć zawartość posiedzenia w PDF"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/proceedings/{id}/{d}/transcripts/pdf')
    res.raise_for_status()
    return res.content

async def async_get_transcript_pdf(session:httpx.AsyncClient, term:int, id:int, d:date, statement_num:int):
    """Zwróć zawartość posiedzenia w PDF"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/proceedings/{id}/{d}/transcripts/{statement_num}')
    res.raise_for_status()
    return res.text

def get_statement_html(session:httpx.Client, term:int, id:int, d:date):
    """Zwróć zawartość oświadczenia w HTML"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/proceedings/{id}/{d}/transcripts/pdf')
    res.raise_for_status()
    return res.content

async def async_get_statement_html(session:httpx.AsyncClient, term:int, id:int, d:date):
    """Zwróć zawartość oświadczenia w HTML"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/proceedings/{id}/{d}/transcripts/pdf')
    res.raise_for_status()
    return res.content

__all__ = ["Proceeding", 'get_proceedings', 'get_proceeding', 'async_get_proceedings', 'async_get_proceeding',
           'StatementList', 'Statement', 'get_transcript', 'async_get_transcript', 'get_statement_html', 'async_get_statement_html',
           'get_transcript_pdf', 'async_get_transcript_pdf']