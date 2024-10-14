from .utils import BASE_URL, filter_query_params, parse_iso_format
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

    def __str__(self):
        return f'Video(video_link={self.video_link})'


def get_videos(session:httpx.Client, term:int, offset:int=None, limit:int=None):
    params = filter_query_params(offset=offset, limit=limit)
    res = session.get(f'{BASE_URL}/sejm/term{term}/videos', params=params)
    res.raise_for_status()
    return list(map(lambda d:Video(d), res.json()))

def get_today_videos(session:httpx.Client, term:int):
    res = session.get(f'{BASE_URL}/sejm/term{term}/videos/today')
    res.raise_for_status()
    return list(map(lambda d: Video(d), res.json()))

async def async_get_videos(session: httpx.AsyncClient, term: int, offset: int = None, limit: int = None):
    params = filter_query_params(offset=offset, limit=limit)
    res = await session.get(f'{BASE_URL}/sejm/term{term}/videos', params=params)
    res.raise_for_status()
    return list(map(lambda d: Video(d), res.json()))

async def async_get_today_videos(session: httpx.AsyncClient, term: int):
    res = await session.get(f'{BASE_URL}/sejm/term{term}/videos/today')
    res.raise_for_status()
    return list(map(lambda d: Video(d), res.json()))

__all__ = ['Video', 'get_videos', 'get_today_videos', 'async_get_videos', 'async_get_today_videos']
