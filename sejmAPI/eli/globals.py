from enum import StrEnum

from .utils import BASE_URL, filter_query_params
from .acts import Acts
from datetime import datetime
import httpx

class ReferencesEnum(StrEnum):
    AKTY_WYKONAWCZE_Z_ART = "Akty wykonawcze z art."
    NOWELIZACJE_PO_TEKSCIE_JEDNOLITYM = "Nowelizacje po tekście jednolitym"
    ORZECZENIE_TK = "Orzeczenie TK"
    AKTY_WYKONAWCZE = "Akty wykonawcze"
    ODESLANIA = "Odesłania"
    SPROSTOWANIE = "Sprostowanie"
    TEKST_JEDNOLITY_DLA_AKTU = "Tekst jednolity dla aktu"
    UCHYLENIA_WYNIKAJACE_Z = "Uchylenia wynikające z"
    AKTY_UZNANE_ZA_UCHYLONE = "Akty uznane za uchylone"
    PRZEPISY_WPROWADZANE = "Przepisy wprowadzane"
    PODSTAWA_PRAWNA = "Podstawa prawna"
    PODSTAWA_PRAWNA_Z_ART = "Podstawa prawna z art."
    ORZECZENIE_TK_DLA_AKTU = "Orzeczenie TK dla aktu"
    AKTY_ZMIENIAJACE = "Akty zmieniające"
    AKTY_ZMIENIONE = "Akty zmienione"
    AKTY_UCHYLONE = "Akty uchylone"
    PRZEPISY_WPROWADZAJACE = "Przepisy wprowadzające"
    AKTY_UCHYLAJACE = "Akty uchylające"
    INF_O_TEKSCIE_JEDNOLITYM = "Inf. o tekście jednolitym"
    SPROSTOWANIE_DLA_AKTOW = "Sprostowanie dla aktów"

def get_all_endpoints(session:httpx.Client):
    """Zwraca endpointy API"""
    res = session.get(f'{BASE_URL}/')
    res.raise_for_status()
    return res.json()

async def async_get_all_endpoints(session:httpx.AsyncClient):
    """Zwraca endpointy API"""
    res = await session.get(f'{BASE_URL}/')
    res.raise_for_status()
    return res.json()

def get_changed_acts(session:httpx.Client, since:datetime, limit:int=None, offset:int=None):
    """Pobierz zmienione akty"""
    params = filter_query_params(since=since.strftime('%Y-%m-%dT%H:%M:%S'), limit=limit, offset=offset)
    res = session.get(f'{BASE_URL}/changes/acts', params=params)
    res.raise_for_status()
    return Acts(res.json())

async def async_get_changed_acts(session:httpx.AsyncClient, since:datetime, limit:int=None, offset:int=None):
    """Pobierz zmienione akty"""
    params = filter_query_params(since=since.strftime('%Y-%m-%dT%H:%M:%S'), limit=limit, offset=offset)
    res = await session.get(f'{BASE_URL}/changes/acts', params=params)
    res.raise_for_status()
    return Acts(res.json())

def get_institutions(session:httpx.Client):
    """Zwróć listę nazw instytucji"""
    res = session.get(f'{BASE_URL}/institutions')
    res.raise_for_status()
    return res.json()

async def async_get_institutions(session:httpx.AsyncClient):
    """Zwróć listę nazw instytucji"""
    res = await session.get(f'{BASE_URL}/institutions')
    res.raise_for_status()
    return res.json()

def get_keywords(session:httpx.Client):
    """Zwróć listę słów kluczowych"""
    res = session.get(f'{BASE_URL}/keywords')
    res.raise_for_status()
    return res.json()

async def async_get_keywords(session:httpx.AsyncClient):
    """Zwróć listę słów kluczowych"""
    res = await session.get(f'{BASE_URL}/keywords')
    res.raise_for_status()
    return res.json()

def get_references(session:httpx.Client):
    """Zwróć listę typów referencji"""
    res = session.get(f'{BASE_URL}/references')
    res.raise_for_status()
    return res.json()

async def async_get_references(session:httpx.AsyncClient):
    """Zwróć listę typów referencji"""
    res = await session.get(f'{BASE_URL}/references')
    res.raise_for_status()
    return res.json()

def get_statuses(session:httpx.Client):
    """Zwróć listę statusów, które może mieć act"""
    res = session.get(f'{BASE_URL}/statuses')
    res.raise_for_status()
    return res.json()

async def async_get_statuses(session:httpx.AsyncClient):
    """Zwróć listę statusów, które może mieć act"""
    res = await session.get(f'{BASE_URL}/statuses')
    res.raise_for_status()
    return res.json()

def get_titles(session:httpx.Client, query:str):
    """Zwraca listę słów znajdujących się w tytułach aktów na bazie parametru query"""
    res = session.get(f'{BASE_URL}/titles', params={'q':query})
    res.raise_for_status()
    return res.json()

async def async_get_titles(session:httpx.AsyncClient, query:str):
    """Zwraca listę słów znajdujących się w tytułach aktów na bazie parametru query"""
    res = await session.get(f'{BASE_URL}/titles', params={'q':query})
    res.raise_for_status()
    return res.json()

def get_types(session:httpx.Client):
    """Zwróć listę typów, które może mieć dokument"""
    res = session.get(f'{BASE_URL}/types')
    res.raise_for_status()
    return res.json()

async def async_get_types(session:httpx.AsyncClient):
    """Zwróć listę typów, które może mieć dokument"""
    res = await session.get(f'{BASE_URL}/types')
    res.raise_for_status()
    return res.json()

__all__ = ['get_types', 'get_titles', 'get_statuses', 'get_references', 'get_all_endpoints', 'get_keywords', 'get_institutions', 'get_changed_acts', 'async_get_types',
           'async_get_titles', 'async_get_statuses', 'async_get_references', 'async_get_keywords', 'async_get_institutions', 'async_get_all_endpoints', 'async_get_changed_acts', 'ReferencesEnum']