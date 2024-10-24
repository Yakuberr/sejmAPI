from datetime import datetime
from enum import StrEnum

BASE_URL = 'https://api.sejm.gov.pl/eli'

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

def filter_query_params(**kwargs):
    """Filtruje podane wartości w parametrach. Tworzy słownik parametrów, które nie mają wartości None"""
    return {k.replace('_',''): str(v) for k, v in kwargs.items() if v is not None}

def parse_iso_format(date_str:str):
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None

def parse_normal_date(date_str:str, format:str):
    try:
        return datetime.strptime(date_str, format).date()
    except ValueError:
        return None

__all__ = ['BASE_URL', 'filter_query_params', 'parse_iso_format', 'parse_normal_date']