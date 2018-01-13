from bs4 import BeautifulSoup, SoupStrainer
import datetime
from pytz import timezone, utc
from .consts import EXPECTED_PB_TIME


def extract_date(date_str, tz='US/Chicago'):
    nd = date_str.replace('st ', ' ').replace('th ', ' ').replace(' of ', ' ')
    nd = nd.replace('rd ', ' ').replace('nd ', ' ').replace('Augu', 'August')
    dt = datetime.datetime.strptime(nd, EXPECTED_PB_TIME)
    dt_loc = timezone(tz).localize(dt)
    return dt_loc.astimezone(utc).isoformat()


def not_these(text, these=[]):
    return text not in these


def has_attr(node, attr='href'):
    return node.get(attr, None) is not None


def extract_pastes_titles(content):
    these = ['/scraping', '/messages', '/settings']

    _tables = BeautifulSoup(content, 'html.parser',
                            parse_only=SoupStrainer('table'))
    for t in _tables.find_all():
        if has_attr(t, 'class'):
            content = str(t)
            break

    _hrefs = BeautifulSoup(content, 'html.parser',
                           parse_only=SoupStrainer('a'))
    hrefs = [i.get('href') for i in _hrefs.find_all() if has_attr(i, 'href')]
    hrefs = [i for i in hrefs if len(i) == 9 and i[1:].isalnum()]
    hrefs = [i for i in hrefs if not_these(i, these=these)]

    pastes_titles = [[i['href'].strip('/'), i.text] for i in _hrefs.find_all()
                     if has_attr(i, 'href') and i['href'] in hrefs]
    return pastes_titles
