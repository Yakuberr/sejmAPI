from .utils import BASE_URL, parse_normal_date
from enum import StrEnum
import httpx

class Group:
    def __init__(self, raw:dict):
        self.id = raw.get('id', '')
        self.name = raw.get('name', '')
        self.eng_name = raw.get('engName', '')
        self.appointment_date = parse_normal_date(raw.get('appointmentDate'), '%Y-%m-%d')

    def __str__(self):
        return f'Group(id={self.id}, name={self.name})'

    def __repr__(self):
        return f'Group(id={self.id}, name={self.name})'

class GroupMember:
    class ChairManEnum(StrEnum):
        chairman = 'chairman'
        co_chairman = 'co_chairman'
        deputy_chairman = 'deputy_chairman'
        secretary = 'secretary'
        member = 'member'

    def __init__(self, raw:dict):
        self.id = raw.get('id', -1)
        self.name = raw.get('name', '')
        self.club = raw.get('club', '')
        self.senator = raw.get('senator', False)
        self.type = GroupMember.ChairManEnum(raw.get('type'))
        self.membership_start = parse_normal_date(raw.get('membershipStart', ''), '%Y-%m-%d')
        self.membership_end = parse_normal_date(raw.get('membershipEnd', ''), '%Y-%m-%d')
        self.mandate_end = parse_normal_date(raw.get('mandateEnd', ''), '%Y-%m-%d')

    def __str__(self):
        return f'GroupMember(id={self.id}, name={self.name}, club={self.club})'

    def __repr__(self):
        return f'GroupMember(id={self.id}, name={self.name}, club={self.club})'

class GroupDetails:
    def __init__(self, raw:dict):
        self.id = raw.get('id', '')
        self.name = raw.get('name', '')
        self.eng_name = raw.get('engName', '')
        self.appointment_date = parse_normal_date(raw.get('appointmentDate', ''), '%Y-%m-%d')
        self.remarks = raw.get('remarks', '')
        self.members = [GroupMember(e) for e in raw.get('members', [])]


def get_bilateral_groups(session:httpx.Client, term:int):
    """Zwróć grupy dwustronne"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/bilateralGroups')
    res.raise_for_status()
    return [Group(e) for e in res.json()]

def get_bilateral_group(session:httpx.Client, term:int, id:int):
    """Zwróć informacje na temat grupy dwustronnej"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/bilateralGroups/{id}')
    res.raise_for_status()
    return GroupDetails(res.json())

async def async_get_bilateral_groups(session:httpx.AsyncClient, term:int):
    """Zwróć grupy dwustronne"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/bilateralGroups')
    res.raise_for_status()
    return [Group(e) for e in res.json()]

async def async_get_bilateral_group(session:httpx.AsyncClient, term:int, id:int):
    """Zwróć informacje na temat grupy dwustronnej"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/bilateralGroups/{id}')
    res.raise_for_status()
    return GroupDetails(res.json())

__all__ = ['Group', 'GroupMember', 'GroupDetails', 'get_bilateral_group', 'get_bilateral_groups', 'async_get_bilateral_group', 'async_get_bilateral_groups']