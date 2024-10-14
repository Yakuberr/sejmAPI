from .utils import BASE_URL, parse_normal_date
import httpx

class Mp:
    def __init__(self, raw: dict):
        self.accusative_name = raw['accusativeName']
        self.active = raw['active']
        self.birth_date = parse_normal_date(raw['birthDate'], '%Y-%m-%d').date()
        self.birth_location = raw['birthLocation']
        self.club = raw['club']
        self.district_name = raw['districtName']
        self.district_num = raw['districtNum']
        self.education_level = raw['educationLevel']
        self.email = raw['email']
        self.first_last_name = raw['firstLastName']
        self.first_name = raw['firstName']
        self.genitive_name = raw['genitiveName']
        self.id = raw['id']
        self.last_first_name = raw['lastFirstName']
        self.last_name = raw['lastName']
        self.number_of_votes = raw['numberOfVotes']
        self.profession = raw.get('profession', '')
        self.second_name = raw.get('secondName', '')
        self.voivodeship = raw['voivodeship']

    def build_photo_uri(self, term:int):
        return f'{BASE_URL}/sejm/term{term}/MP/{self.id}/photo'

    def build_mini_photo_uri(self, term:int):
        return f'{BASE_URL}/sejm/term{term}/MP/{self.id}/photo-mini'

    def __str__(self):
        return f'{self.first_last_name} ({self.birth_date}, {self.birth_location}), {self.club}'

def get_mps(session:httpx.Client, term:int):
    res = session.get(f'{BASE_URL}/sejm/term{term}/MP')
    res.raise_for_status()
    return list(map(lambda d:Mp(d), res.json()))

def get_mp_photo(session:httpx.Client, uri:str):
    """Zdjęcie powinno być pobrane w rozszerzeniu .jfif"""
    res = session.get(uri)
    res.raise_for_status()
    return res.content

async def async_get_mps(session:httpx.AsyncClient, term:int):
    res = await session.get(f'{BASE_URL}/sejm/term{term}/MP')
    res.raise_for_status()
    return list(map(lambda d: Mp(d), res.json()))

async def async_get_mp_photo(session:httpx.AsyncClient, uri:str):
    """Zdjęcie powinno być pobrane w rozszerzeniu .jfif"""
    res = await session.get(uri)
    res.raise_for_status()
    return res.content

__all__ = ['Mp', 'get_mps', 'get_mp_photo', 'async_get_mps', 'async_get_mp_photo']
