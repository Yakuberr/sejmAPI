from .utils import BASE_URL
import httpx

class Club:
    def __init__(self, raw: dict):
        self.email = raw.get('email', '')
        self.fax = raw.get('fax', '')
        self.id = raw.get('id', '')
        self.members_count = raw.get('membersCount', -1)
        self.name = raw.get('name', '')
        self.phone = raw.get('phone', '')  # Pole phone może być puste, więc obsługujemy to domyślną wartością

    def build_logo_uri(self, term:int):
        return f'{BASE_URL}/sejm/term{term}/clubs/{self.id}/logo'

    def __str__(self):
        return f'Club: {self.name} (ID: {self.id}, Members: {self.members_count})'

    def __repr__(self):
        return f'Club: {self.name} (ID: {self.id}, Members: {self.members_count})'


def get_clubs(session:httpx.Client, term:int):
    """Pobierz informacje o klubach"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/clubs')
    res.raise_for_status()
    return list(map(lambda d:Club(d), res.json()))

def get_club(session:httpx.Client, term:int, id:str):
    """Pobierz informacje o klubie"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/clubs/{id}')
    res.raise_for_status()
    return Club(res.json())

def get_logo(session:httpx.Client, uri:str):
    """Zdjęcie powinno być pobrane w rozszerzeniu .jfif"""
    res = session.get(uri)
    res.raise_for_status()
    return res.content

async def async_get_clubs(session:httpx.AsyncClient, term:int):
    """Pobierz informacje o klubach"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/clubs')
    res.raise_for_status()
    return list(map(lambda d:Club(d), res.json()))

async def async_get_club(session:httpx.AsyncClient, term:int, id:str):
    """Pobierz informacje o klubie"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/clubs/{id}')
    res.raise_for_status()
    return Club(res.json())

async def async_get_logo(session:httpx.AsyncClient, uri:str):
    """Zdjęcie powinno być pobrane w rozszerzeniu .jfif"""
    res = await session.get(uri)
    res.raise_for_status()
    return res.content

__all__ = ['Club', 'get_clubs', 'get_club', 'get_logo', 'async_get_club', 'async_get_clubs', 'async_get_logo']
