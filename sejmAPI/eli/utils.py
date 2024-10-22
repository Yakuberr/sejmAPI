from datetime import datetime
BASE_URL = 'https://api.sejm.gov.pl/eli'

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