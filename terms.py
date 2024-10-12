from datetime import datetime
from exceptions import invalidLinkException
import httpx

DEFAULT_ENDPOINT = '/sejm/term'

class Prints:
    def __init__(self, raw):
        self.raw = raw

    @property
    def count(self):
        return self.raw['count']

    @property
    def last_changed(self):
        return datetime.fromisoformat(self.raw['lastChanged'])

    @property
    def link(self):
        if type(self.raw['link'] is bool):
            raise invalidLinkException("Invalid term's print link")
        return self.raw['link']

    def build_uri(self):
        return f'https://api.sejm.gov.pl/sejm{self.link}'


class Term:
    def __init__(self, raw):
        self.raw = raw

    @property
    def current(self):
        return self.raw['current']

    @property
    def start(self):
        return datetime.strptime(self.raw['from'], '%Y-%m-%d').date()

    @property
    def num(self):
        return self.raw['num']

    @property
    def prints(self):
        return Prints(self.raw['prints'])

    def __str__(self):
        return f'<{self.num}, {self.start}>'

def get_current_term(client:httpx.Client):
    try:
        return Term(httpx.get(f'https://api.sejm.gov.pl{DEFAULT_ENDPOINT}').json()[-1])
    except httpx.RequestError as exc:
        print(f'Error occurred while requesting data: {exc}')
    except KeyError as exc:
        print(f'Invalid response structure: {exc}')

