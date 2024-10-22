from .utils import BASE_URL, filter_query_params
from datetime import date, datetime
import httpx

class PublishigHouse:
    def __init__(self, raw:dict):
        self.code = raw.get('code', '')
        self.short_name = raw.get('shortName', '')
        self.name = raw.get('name', '')
        self.acts_count = raw.get('actsCount', -1)
        self.years = raw.get('years', [])

class Acts:
    def __init__(self, raw:dict):
        self.items = raw.get('items', '') # TODO: to powinna być lista obiektów klasy ActInfo
        self.offset = raw.get('offset', -1)
        self.count = raw.get('count', -1)
        self.total_count = raw.get('totalCount', -1)
        # TODO: Można tu kiedyś dodać obiekt możliwej klasy searchQuery

def get_publishers(session:httpx.Client):
    """Zwraca listę wydawców"""
    res = session.get(f'{BASE_URL}/acts')
    res.raise_for_status()
    return [PublishigHouse(p) for p in res.json()]

async def async_get_publishers(session:httpx.AsyncClient):
    """Zwraca listę wydawców"""
    res = await session.get(f'{BASE_URL}/acts')
    res.raise_for_status()
    return [PublishigHouse(p) for p in res.json()]

# TODO: parametr act_type jest prawdopodobnie enumem
def search_acts(session:httpx.Client, announcement_date:date=None, date_effect:date=None, date_effect_from:date=None, date_effect_to:date=None,
                date_from:date=None, date_to:date=None, exile:str=None, in_force:str=None, keyword:str=None, limit:int=None, offset:int=None,
                position:int=None, pub_date:date=None, pub_date_from:date=None, pub_date_to:date=None, publisher:str=None, title:str=None,
                act_ype:str=None, volume:int=None, year:int=None):
    params = filter_query_params(announcement_date=announcement_date, date_effect=date_effect, date_effect_from=date_effect_from, date_effect_to=date_effect_to,
        date_from=date_from, date_to=date_to, exile=exile, in_force=in_force, keyword=keyword, limit=limit, offset=offset,
        position=position, pub_date=pub_date, pub_date_from=pub_date_from, pub_date_to=pub_date_to, publisher=publisher, title=title,
        act_ype=act_ype, volume=volume, year=year)
    res = session.get(f'{BASE_URL}/acts/search', params=params)
    res.raise_for_status()
    return res.json()