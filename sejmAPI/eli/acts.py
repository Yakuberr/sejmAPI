from enum import StrEnum
from .utils import BASE_URL, filter_query_params, parse_normal_date, parse_iso_format, ReferencesEnum
from datetime import date, datetime
import httpx

class Directive:
    def __init__(self, raw:dict):
        self.address = raw.get('address', '')
        self.title = raw.get('title', '')
        self.date = parse_normal_date(raw.get('date', ''), '%Y-%m-%d')

class PublishigHouse:
    def __init__(self, raw:dict):
        self.code = raw.get('code', '')
        self.short_name = raw.get('shortName', '')
        self.name = raw.get('name', '')
        self.acts_count = raw.get('actsCount', -1)
        self.years = raw.get('years', [])

class ActInfo:
    def __init__(self, raw:dict):
        self.address = raw.get('address', '')
        self.publisher = raw.get('publisher', '')
        self.year = raw.get('year', -1)
        self.volume = raw.get('volume', -1)
        self.pos = raw.get('pos', -1)
        self.title = raw.get('title', '')
        self.display_address = raw.get('displayAddress', '')
        self.promulgation = parse_normal_date(raw.get('promulgation', ''), '%Y-%m-%d')
        self.announcement_date = parse_normal_date(raw.get('announcementDate', ''), '%Y-%m-%d')
        self.textPDF = raw.get('textPDF', False)
        self.textHTML = raw.get('textHTML', False)
        self.change_date = parse_iso_format(raw.get('changeDate', ''))
        self.eli = raw.get('ELI', '')
        self.act_type = raw.get('type', '')
        self.status = raw.get('status', '')

class ActText:
    class ActTextTypeEnum(StrEnum):
        t = 'T'
        o='O'
        u='U'
        h='H'
        i='I'
    def __init__(self, raw:dict):
        self.filename = raw.get('filename', '')
        self.type_ = ActText.ActTextTypeEnum(raw.get('type'))

class PrintRef:
    def __init__(self, raw:dict):
        self.term = raw.get('term', -1)
        self.number = raw.get('number', '')
        self.link = raw.get('link', '')
        self.link_print_api = raw.get('linkPrintAPI', '')
        self.link_process_api = raw.get('linkProcessAPI', '')

class ReferenceInfo:
    def __init__(self, raw:dict):
        self.id	= raw.get('id', '')
        self.art = raw.get('art', '')
        self.date = parse_normal_date(raw.get('date', ''), '%Y-%m-%d')


class Act:

    @staticmethod
    def _create_references(raw:dict):
        fd = {}
        if len(raw.keys()) == 0:
            return fd
        for ref in ReferencesEnum:
            references_list =  raw.get(ref, [])
            fd.update({ref:list(map(lambda d:ReferenceInfo(d), references_list))})
        return fd

    class ActInForceEnum(StrEnum):
        in_force='IN_FORCE'
        not_in_force = 'NOT_IN_FORCE'
        unknown = 'UNKNOWN'

    def __init__(self, raw:dict):
        self.address = raw.get('address', '')
        self.publisher = raw.get('publisher', '')
        self.year = raw.get('year', -1)
        self.volume = raw.get('volume', -1)
        self.pos = raw.get('pos', -1)
        self.title = raw.get('title', '')
        self.display_address = raw.get('displayAddress', '')
        self.promulgation = parse_normal_date(raw.get('promulgation', ''), '%Y-%m-%d')
        self.announcement_date = parse_normal_date(raw.get('announcementDate', ''), '%Y-%m-%d')
        self.textPDF = raw.get('textPDF', False)
        self.textHTML = raw.get('textHTML', False)
        self.change_date = parse_iso_format(raw.get('changeDate', ''))
        self.eli = raw.get('ELI', '')
        self.act_type = raw.get('type', '')
        self.status = raw.get('status', '')
        self.entry_into_force = parse_normal_date(raw.get('entryIntoForce', ''), '%Y-%m-%d')
        self.valid_from = parse_normal_date(raw.get('validFrom', ''), '%Y-%m-%d')
        self.repeal_date = parse_normal_date(raw.get('repealDate', ''), '%Y-%m-%d')
        self.expiration_date = parse_normal_date(raw.get('expirationDate', ''), '%Y-%m-%d')
        self.legal_status_date = parse_normal_date(raw.get('legalStatusDate', ''), '%Y-%m-%d')
        self.in_force = Act.ActInForceEnum(raw.get('inForce'))
        self.comments = raw.get('comments', [])
        self.released_by = raw.get('releasedBy', '')
        # TODO: Pole 'authorizedBody' jest pominięte
        self.obligated = raw.get('obligated', '')
        self.directives = [Directive(d) for d in raw.get('directives', [])]
        self.keywords = raw.get('keywords', [])
        self.keywords_names = raw.get('keywordsNames', [])
        self.texts = [ActText(at) for at in raw.get('texts', [])]
        self.previous_title = raw.get('previousTitle', [])
        self.prints = [PrintRef(p) for p in raw.get('prints', [])]
        self.references = self._create_references(raw.get('references', {}))






class Acts:
    def __init__(self, raw:dict):
        self.items = [Act(a) for a in raw.get('items', [])]
        self.offset = raw.get('offset', -1)
        self.count = raw.get('count', -1)
        self.total_count = raw.get('totalCount', -1)
        # TODO: Można tu kiedyś dodać obiekt możliwej klasy searchQuery

class ActsInfo:
    def __init__(self, raw:dict):
        self.items = [ActInfo(ai) for ai in raw.get('items', [])]
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
    """Wyszukaj akt na podstawie parametrów"""
    params = filter_query_params(announcement_date=announcement_date, date_effect=date_effect, date_effect_from=date_effect_from, date_effect_to=date_effect_to,
        date_from=date_from, date_to=date_to, exile=exile, in_force=in_force, keyword=keyword, limit=limit, offset=offset,
        position=position, pub_date=pub_date, pub_date_from=pub_date_from, pub_date_to=pub_date_to, publisher=publisher, title=title,
        act_ype=act_ype, volume=volume, year=year)
    res = session.get(f'{BASE_URL}/acts/search', params=params)
    res.raise_for_status()
    return Acts(res.json())

# TODO: parametr act_type jest prawdopodobnie enumem
async def async_search_acts(session:httpx.AsyncClient, announcement_date:date=None, date_effect:date=None, date_effect_from:date=None, date_effect_to:date=None,
                date_from:date=None, date_to:date=None, exile:str=None, in_force:str=None, keyword:str=None, limit:int=None, offset:int=None,
                position:int=None, pub_date:date=None, pub_date_from:date=None, pub_date_to:date=None, publisher:str=None, title:str=None,
                act_ype:str=None, volume:int=None, year:int=None):
    """Wyszukaj akt na podstawie parametrów"""
    params = filter_query_params(announcement_date=announcement_date, date_effect=date_effect, date_effect_from=date_effect_from, date_effect_to=date_effect_to,
        date_from=date_from, date_to=date_to, exile=exile, in_force=in_force, keyword=keyword, limit=limit, offset=offset,
        position=position, pub_date=pub_date, pub_date_from=pub_date_from, pub_date_to=pub_date_to, publisher=publisher, title=title,
        act_ype=act_ype, volume=volume, year=year)
    res = await session.get(f'{BASE_URL}/acts/search', params=params)
    res.raise_for_status()
    return Acts(res.json())

def get_publisher_info(session:httpx.Client, publisher:str):
    """Zwraca informacje na temat wydawcy"""
    res = session.get(f'{BASE_URL}/acts/{publisher}')
    res.raise_for_status()
    return PublishigHouse(res.json())

async def async_get_publisher_info(session:httpx.AsyncClient, publisher:str):
    """Zwraca informacje na temat wydawcy"""
    res = await session.get(f'{BASE_URL}/acts/{publisher}')
    res.raise_for_status()
    return PublishigHouse(res.json())

def get_acts_for_year(session:httpx.Client, publisher:str, year:int):
    """Zwraca Akty dla danego roku i wydawcy"""
    res = session.get(f'{BASE_URL}/acts/{publisher}/{year}')
    res.raise_for_status()
    return ActsInfo(res.json())

async def async_get_acts_for_year(session:httpx.AsyncClient, publisher:str, year:int):
    """Zwraca Akty dla danego roku i wydawcy"""
    res = await session.get(f'{BASE_URL}/acts/{publisher}/{year}')
    res.raise_for_status()
    return ActsInfo(res.json())

def get_volumes(session:httpx.Client, publisher:str, year:int):
    """Zwraca listę tomów dla danego wydawcy i roku"""
    res = session.get(f'{BASE_URL}/acts/{publisher}/{year}/volumes')
    res.raise_for_status()
    return res.json()

async def async_get_volumes(session:httpx.AsyncClient, publisher:str, year:int):
    """Zwraca listę tomów dla danego wydawcy i roku"""
    res = await session.get(f'{BASE_URL}/acts/{publisher}/{year}/volumes')
    res.raise_for_status()
    return res.json()

def get_acts_for_volume(session:httpx.Client, publisher:str, year:int, volume:int):
    """Zwraca listę tomów dla danego wydawcy i roku"""
    res = session.get(f'{BASE_URL}/acts/{publisher}/{year}/volumes/{volume}')
    res.raise_for_status()
    return ActsInfo(res.json())

async def async_get_acts_for_volume(session:httpx.AsyncClient, publisher:str, year:int, volume:int):
    """Zwraca listę tomów dla danego wydawcy i roku"""
    res = await session.get(f'{BASE_URL}/acts/{publisher}/{year}/volumes/{volume}')
    res.raise_for_status()
    return ActsInfo(res.json())

def get_act_details(session:httpx.Client, publisher:str, year:int, position:int):
    """Zwróć szczegóły na temat konkretnego aktu"""
    res = session.get(f'{BASE_URL}/acts/{publisher}/{year}/{position}')
    res.raise_for_status()
    return Act(res.json())

async def async_get_act_details(session:httpx.AsyncClient, publisher:str, year:int, position:int):
    """Zwróć szczegóły na temat konkretnego aktu"""
    res = await session.get(f'{BASE_URL}/acts/{publisher}/{year}/{position}')
    res.raise_for_status()
    return Act(res.json())

def get_act_references(session:httpx.Client, publisher:str, year:int, position:int):
    """Zwróć referencje do danego aktu"""
    res = session.get(f'{BASE_URL}/acts/{publisher}/{year}/{position}/references')
    res.raise_for_status()
    return Act._create_references(res.json())

async def async_get_act_references(session:httpx.AsyncClient, publisher:str, year:int, position:int):
    """Zwróć referencje do danego aktu"""
    res = await session.get(f'{BASE_URL}/acts/{publisher}/{year}/{position}/references')
    res.raise_for_status()
    return Act._create_references(res.json())

# TODO: DO ogarnięcia funkcja pobierająca dane z /acts/{publisher}/{year}/{position}/struct oraz enkapsulacja danych w klasę

def get_act_text(session:httpx.Client, publisher:str, year:int, position:int):
    """Zwróć text aktu w HTML"""
    res = session.get(f'{BASE_URL}/acts/{publisher}/{year}/{position}/text.html')
    res.raise_for_status()
    return res.text

async def async_get_act_text(session:httpx.AsyncClient, publisher:str, year:int, position:int):
    """Zwróć text aktu w HTML"""
    res = await session.get(f'{BASE_URL}/acts/{publisher}/{year}/{position}/text.html')
    res.raise_for_status()
    return res.text

#TODO: Do ogarnięcia funkcja pobierająca dane z /acts/{publisher}/{year}/{position}/text.html/{tree}

def get_act_pdf(session:httpx.Client, publisher:str, year:int, position:int):
    """Zwróć akt w postaci PDF"""
    res = session.get(f'{BASE_URL}/acts/{publisher}/{year}/{position}/text.pdf')
    res.raise_for_status()
    return res.content

async def async_get_act_pdf(session:httpx.AsyncClient, publisher:str, year:int, position:int):
    """Zwróć akt w postaci PDF"""
    res = await session.get(f'{BASE_URL}/acts/{publisher}/{year}/{position}/text.pdf')
    res.raise_for_status()
    return res.content

# TODO: Endpoint /acts/{publisher}/{year}/{position}/text/{type}/{fileName} zdaje się nie działać

__all__ = ['Directive', 'PublishigHouse', 'ActInfo', 'ActText', 'PrintRef', 'ReferenceInfo', 'Act', 'Acts', 'ActsInfo', 'get_act_pdf', 'get_act_references',
           'get_act_text', 'get_act_details', 'get_acts_for_year', 'get_acts_for_volume', 'get_volumes', 'get_publisher_info', 'get_publishers', 'async_get_act_text',
           'async_get_act_pdf', 'async_get_act_references', 'async_search_acts', 'async_get_volumes', 'async_get_act_details', 'async_get_acts_for_year', 'async_get_acts_for_volume',
           'async_get_publisher_info', 'async_get_publishers', 'search_acts']
