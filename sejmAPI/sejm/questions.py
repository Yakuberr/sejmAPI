from cgi import parse
from enum import StrEnum

import httpx
from .utils import BASE_URL, filter_query_params, parse_normal_date, parse_iso_format
from datetime import date

class SortQuestionByEnum(StrEnum):
    last_modified = 'lastModified'

class Link:
    def __init__(self, raw:dict):
        self.href = raw.get('href', '')
        self.rel = raw.get('rel', '')

class Attachment:
    def __init__(self, raw:dict):
        self.name = raw.get('name', '')
        self.url = raw.get('URL', '')
        self.last_modified = parse_iso_format(raw.get('lastModified', ''))


class Reply:
    def __init__(self, raw:dict):
        self.key = raw.get('key')
        self.receipt_date = parse_normal_date(raw.get('receiptDate', ''), '%Y-%m-%d')
        self.last_modified = parse_iso_format(raw.get('lastModified', ''))
        self.from_ = raw.get('from', '')
        self.links = [Link(l) for l in raw.get('links')]
        self.only_attachment = raw.get('onlyAttachment', False)
        self.attachments = [Attachment(a) for a in raw.get('attachments', [])]

class Question:
    def __init__(self, raw:dict):
        self.term = raw.get('term', -1)
        self.num = raw.get('num', -1)
        self.title = raw.get('title', '')
        self.receipt_date = parse_normal_date(raw.get('receiptDate', ''), '%Y-%m-%d')
        self.last_modified = parse_iso_format(raw.get('lastModified', ''))
        self.links = [Link(l) for l in raw.get('links')]
        self.from_ = raw.get('from', [])
        self.to = raw.get('to', [])
        self.send_date = parse_normal_date(raw.get('sentDate', ''), '%Y-%m-%d')
        self.replies = [Reply(r) for r in raw.get('replies',[])]



def get_written_questions(session:httpx.Client, term:int, from_:date=None, limit:int=None, modifiedSince:str=None, offset:int=None, since:date=None,
                         till:date=None, title:str=None, to:str=None, sort_by:SortQuestionByEnum=None, descending=False):
    """Pobiera listę pytań
    UWAGA: Zbyt duża ilość parametrów wywołuje błąd 403"""
    params = filter_query_params(from_=from_, limit=limit, modifiedSince=modifiedSince, offset=offset, since=since, till=till, title=title, to=to)
    DESCENDING_MAP = {
        True:'-',
        False:''
    }
    if sort_by != '':
        params['sort_by'] = f'{DESCENDING_MAP[descending]}{sort_by}'
    res = session.get(f'{BASE_URL}/sejm/term{term}/writtenQuestions', params=params)
    res.raise_for_status()
    return [Question(q) for q in res.json()]

async def async_get_written_questions(session:httpx.AsyncClient, term:int, from_:date=None, limit:int=None, modifiedSince:str=None, offset:int=None, since:date=None,
                         till:date=None, title:str=None, to:str=None, sort_by:SortQuestionByEnum=None, descending=False):
    """Pobiera listę pytań
    UWAGA: Zbyt duża ilość parametrów wywołuje błąd 403"""
    params = filter_query_params(from_=from_, limit=limit, modifiedSince=modifiedSince, offset=offset, since=since, till=till, title=title, to=to)
    DESCENDING_MAP = {
        True:'-',
        False:''
    }
    if sort_by != '':
        params['sort_by'] = f'{DESCENDING_MAP[descending]}{sort_by}'
    res = await session.get(f'{BASE_URL}/sejm/term{term}/writtenQuestions', params=params)
    res.raise_for_status()
    return [Question(q) for q in res.json()]

def get_question(session:httpx.Client, term:int, num:int):
    """Zwróć dane na temat pytania"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/writtenQuestion/{num}')
    res.raise_for_status()
    return Question(res.json())

async def async_get_question(session:httpx.AsyncClient, term:int, num:int):
    """Zwróć dane na temat pytania"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/writtenQuestion/{num}')
    res.raise_for_status()
    return Question(res.json())

def get_question_html(session:httpx.Client, term:int, num:int):
    """Zwróć pytanie w formie HTML"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/writtenQuestion/{num}/html')
    res.raise_for_status()
    return res.text

async def async_get_question_html(session:httpx.AsyncClient, term:int, num:int):
    """Zwróć pytanie w formie HTML"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/writtenQuestion/{num}/html')
    res.raise_for_status()
    return res.text

def get_question_reply_html(session:httpx.Client, term:int, num:int, key:str):
    """Zwróć odpowiedź na pytanie w formie HTML"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/writtenQuestion/{num}/reply/{key}/body')
    res.raise_for_status()
    return res.text

async def async_get_question_reply_html(session:httpx.AsyncClient, term:int, num:int, key:str):
    """Zwróć odpowiedź na pytanie w formie HTML"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/writtenQuestion/{num}/reply/{key}/body')
    res.raise_for_status()
    return res.text

__all__ = ['SortQuestionByEnum', 'Link', 'Attachment', 'Reply', "Question", 'get_question', 'get_question_html', 'get_question_reply_html',
           'async_get_question_html', 'async_get_question', 'async_get_written_questions', 'async_get_question_reply_html', 'get_written_questions']