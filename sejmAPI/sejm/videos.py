from .utils import BASE_URL, filter_query_params, parse_iso_format
from datetime import date
import httpx

class Video:
    def __init__(self, raw: dict):
        self.committee = raw.get('committee', '')  # Nazwa komisji
        self.description = raw.get('description', '')  # Opis wydarzenia
        self.end_date_time = parse_iso_format(raw.get('endDateTime', ''))  # Czas zakończenia
        self.room = raw.get('room', '')  # Sala, w której odbywa się wydarzenie
        self.start_date_time = parse_iso_format(raw.get('startDateTime', ''))  # Czas rozpoczęcia
        self.title = raw.get('title', '')  # Tytuł wydarzenia
        self.transcribe = raw.get('transcribe', False)  # Flaga dotycząca transkrypcji
        self.type = raw.get('type', '')  # Typ wydarzenia (np. "komisja")
        self.unid = raw.get('unid', '')  # Unikalny identyfikator
        self.video_link = raw.get('videoLink', '')  # Link do wideo
        self.other_video_links = raw.get('otherVideoLinks', [])
        self.video_messages_link = raw.get('videoMessagesLink', '')
        self.sign_lang_link = raw.get('signLangLink', '')
        self.audio = raw.get('audio', '')

    def __str__(self):
        return f'Video(video_link={self.video_link})'


def get_videos(session:httpx.Client, term:int, offset:int=None, limit:int=None, committee:str=None, since:date=None,till:date=None, title:str=None, committee_type:str=None):
    """Zwraca listę transmisji wideo"""
    params = filter_query_params(offset=offset, limit=limit, committee=committee, till=till, title=title, since=since, committee_type=committee_type)
    res = session.get(f'{BASE_URL}/sejm/term{term}/videos', params=params)
    res.raise_for_status()
    return list(map(lambda d:Video(d), res.json()))

def get_today_videos(session:httpx.Client, term:int):
    """Pobiera listę transmisji wideo dla dzisiejszego dnia"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/videos/today')
    res.raise_for_status()
    return list(map(lambda d: Video(d), res.json()))

async def async_get_videos(session:httpx.AsyncClient, term:int, offset:int=None, limit:int=None, committee:str=None, since:date=None,till:date=None, title:str=None, committee_type:str=None):
    """Zwraca listę transmisji wideo"""
    params = filter_query_params(offset=offset, limit=limit, committee=committee, till=till, title=title, since=since, committee_type=committee_type)
    res = await session.get(f'{BASE_URL}/sejm/term{term}/videos', params=params)
    res.raise_for_status()
    return list(map(lambda d:Video(d), res.json()))

async def async_get_today_videos(session: httpx.AsyncClient, term: int):
    """Pobiera listę transmisji wideo dla dzisiejszego dnia"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/videos/today')
    res.raise_for_status()
    return list(map(lambda d: Video(d), res.json()))

def get_videos_for_date(session:httpx.Client, term:int, d:date):
    """Pobiera listę transmisji wideo dla danej daty"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/videos/{str(d)}')
    res.raise_for_status()
    return list(map(lambda e: Video(e), res.json()))

async def async_get_videos_for_date(session:httpx.AsyncClient, term:int, d:date):
    """Pobiera listę transmisji wideo dla danej daty"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/videos/{str(d)}')
    res.raise_for_status()
    return list(map(lambda e: Video(e), res.json()))

def get_video_details(session:httpx.Client, term:int, unid:str):
    """Zwróć informacje na temat danej transmisji wideo"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/videos/{unid}')
    res.raise_for_status()
    return Video(res.json())

async def async_get_video_details(session:httpx.AsyncClient, term:int, unid:str):
    """Zwróć informacje na temat danej transmisji wideo"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/videos/{unid}')
    res.raise_for_status()
    return Video(res.json())

__all__ = ['Video', 'get_videos', 'get_today_videos', 'async_get_videos', 'async_get_today_videos', 'get_video_details', 'get_videos_for_date',
           'async_get_video_details', 'async_get_videos_for_date']
