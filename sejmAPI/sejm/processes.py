from .utils import BASE_URL, parse_normal_date, parse_iso_format
from enum import StrEnum
import httpx

class ProcessHeader:
    class UeEnum(StrEnum):
        no = 'NO'
        adaptation = 'ADAPTATION'
        enforcement = 'ENFORCEMENT'

    def __init__(self, raw:dict):
        self.uE = ProcessHeader.UeEnum(raw.get('uE'))
        self.term = raw.get('term', -1)
        self.number = raw.get('number', '')
        self.title = raw.get('title', '')
        self.description = raw.get('description', '')
        self.ue = ProcessHeader.UeEnum(raw.get('ue'))
        self.document_date = parse_normal_date(raw.get('documentDate', ''), '%Y-%m-%d')
        self.process_start_date = parse_normal_date(raw.get('processStartDate', ''), '%Y-%m-%d')
        self.change_date = parse_iso_format(raw.get('changeDate', ''))
        self.document_type = raw.get('documentType', '')
        self.comments = raw.get('comments', '')
        self.web_generated_date = parse_iso_format(raw.get('webGeneratedDate', ''))

    def __str__(self):
        return f'ProcessHeader(term={self.term}, number={self.number}, uE={self.uE})'

    def __repr__(self):
        return f'ProcessHeader(term={self.term}, number={self.number}, uE={self.uE})'

class ProcessDocument:
    def __init__(self, raw:dict):
        self.number = raw.get('number', '')
        self.registered_date = parse_normal_date(raw.get('registeredDate', ''), '%Y-%m-%d')

    def __str__(self):
        return f'ProcessDocument(number={self.number}, registered_date={self.registered_date})'

    def __repr__(self):
        return f'ProcessDocument(number={self.number}, registered_date={self.registered_date})'

class ProcessStage:
    def __init__(self, raw:dict):
        self.stage_name = raw.get('stageName', '')
        self.date = parse_normal_date(raw.get('date', ''), '%Y-%m-%d')
        self.children = self._get_children(raw.get('children', []))

    def _get_children(self, raw: list):
        if not raw:
            return []
        return [ProcessStage(child) for child in raw if isinstance(child, dict)]

    def __str__(self):
        return f'ProcessStage(stage_name={self.stage_name}, date={self.date})'

    def __repr__(self):
        return f'ProcessStage(stage_name={self.stage_name}, date={self.date})'

class ProcessDetails:
    class UrgencyStatusEnum(StrEnum):
        normal = 'NORMAL'
        urgent='URGENT'
        urgent_withdrawn = 'URGENT_WITHDRAWN '

    def __init__(self, raw:dict):
        self.uE = ProcessHeader.UeEnum(raw.get('uE'))
        self.term = raw.get('term', -1)
        self.title = raw.get('title', '')
        self.description = raw.get('description', '')
        self.number = raw.get('number', '')
        self.document_date = parse_normal_date(raw.get('documentDate', ''), '%Y-%m-%d')
        self.change_date = parse_iso_format(raw.get('changeDate', ''))
        self.web_generated_date = parse_iso_format(raw.get('webGeneratedDate', ''))
        self.process_start_date = parse_normal_date(raw.get('processStartDate', ''), '%Y-%m-%d')
        self.document_type = raw.get('documentType', '')
        self.comments = raw.get('comments', '')
        self.document_date = parse_normal_date(raw.get('documentDate', ''), '%Y-%m-%d')
        self.other_documents = [ProcessDocument(e) for e in raw.get('otherDocuments', [])]
        self.rcl_num = raw.get('rclNum', '')
        self.urgency_status = ProcessDetails.UrgencyStatusEnum(raw.get('urgencyStatus'))
        self.urgency_withdraw_date = parse_normal_date(raw.get('urgencyWithdrawDate', ''), '%Y-%m-%d')
        self.legislative_committee = raw.get('legislativeCommittee', False)
        self.principle_of_subsidiarity = raw.get('principleOfSubsidiarity', False)
        self.stages = [ProcessStage(e) for e in raw.get('stages', [])]
        self.prints_considered_jointly = raw.get('printsConsideredJointly', [])

    def __str__(self):
        return f'ProcessDetails(title={self.title}, number={self.number}, document_date={self.document_date})'

    def __repr__(self):
        return f'ProcessDetails(title={self.title}, number={self.number}, document_date={self.document_date})'



def get_processes(session:httpx.Client, term:int):
    """Pobierz listę procesór legislacyjnych"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/processes')
    res.raise_for_status()
    return [ProcessHeader(e) for e in res.json()]

def get_process(session:httpx.Client, term:int, num:int):
    """Pobierz informacje na temat procesu legislacyjnego"""
    res = session.get(f'{BASE_URL}/sejm/term{term}/processes/{num}')
    res.raise_for_status()
    return ProcessDetails(res.json())

async def async_get_processes(session:httpx.AsyncClient, term:int):
    """Pobierz listę procesór legislacyjnych"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/processes')
    res.raise_for_status()
    return [ProcessHeader(e) for e in res.json()]

async def async_get_process(session:httpx.AsyncClient, term:int, num:int):
    """Pobierz informacje na temat procesu legislacyjnego"""
    res = await session.get(f'{BASE_URL}/sejm/term{term}/processes/{num}')
    res.raise_for_status()
    return ProcessDetails(res.json())

__all__ = ['ProcessDetails', 'ProcessStage', 'ProcessHeader', 'ProcessDocument', 'get_process', 'get_processes', 'async_get_process', 'async_get_processes']