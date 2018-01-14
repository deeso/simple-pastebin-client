from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
from pytz import timezone, utc
import tzlocal
from .consts import *


def extract_date_from_html(html_page, tz='US/Central'):
    _span = BeautifulSoup(html_page, 'html.parser',
                          parse_only=SoupStrainer('span'))
    spans = [i for i in _span.find_all() if has_attr(i, 'title')]
    if len(spans) == 1:
        return extract_date(spans[0]['title'], tz=tz)

    # editied
    for s in spans:
        new_title = None
        try:
            new_title = s['title']
            if new_title.find('Last edit on: ') == 0:
                new_title = s['title'].replace('Last edit on: ', '')
                return extract_date(new_title, tz=tz)
        except:
            pass
    for s in spans:
        if 'title' not in s:
            continue
        try:
            return extract_date(s['title'], tz=tz)
        except:
            pass
    return ''


def date_to_timestamp(date_str):
    if date_str == '':
        return -1
    return int(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").timestamp())


def extract_date(date_str, tz='US/Central'):
    tz = tzlocal.get_localzone().zone if tz is None else tz
    nd = date_str.replace('st ', ' ').replace('th ', ' ').replace(' of ', ' ')
    nd = nd.replace('rd ', ' ').replace('nd ', ' ').replace('Augu', 'August')
    dt = datetime.strptime(nd, EXPECTED_PB_TIME)
    dt_loc = timezone(tz).localize(dt)
    return dt_loc.astimezone(utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def extract_elements(html_page, tag, attr, value_in=None):
    tags = BeautifulSoup(html_page, 'html.parser',
                         parse_only=SoupStrainer(tag))

    vals = []
    for i in [j for j in tags.find_all()]:
        if has_attr(i, attr):
            if value_in is None:
                vals.append(i)
            elif value_in in i[attr]:
                vals.append(i)
    return vals


def extract_single_element(html_page, tag, attr, value_in):
    vals = extract_elements(html_page, tag, attr, value_in)
    if len(vals) > 0:
        return vals[0]
    return None


def extract_paste_box_line1(html_page):
    tag, attr, value_in = [DIV, CLASS, PBOX_1]
    v = extract_single_element(html_page, tag, attr, value_in)
    title = '' if v is None else v['title']
    return {'title': title}


def extract_paste_box_line2(html_page, tz="US/Central"):
    tag, attr, value_in = [DIV, CLASS, PBOX_2]
    pbox2 = extract_single_element(html_page, tag, attr, value_in)
    # extract user
    _hrefs = BeautifulSoup(str(pbox2), 'html.parser',
                           parse_only=SoupStrainer('a'))
    pusers = [i.get('href').strip('/u/') for i in _hrefs.find_all()
              if has_attr(i, 'href') and i['href'].find('/u/') == 0]

    user = pusers[0] if len(pusers) > 0 else ''

    # extract date
    date = extract_date_from_html(str(pbox2), tz)
    if date == '':
        print (pbox2)
    unixts = date_to_timestamp(date)
    return {'user': user, 'timestamp': date, 'unix': unixts}


def extract_text_data(html_page):
    textarea = BeautifulSoup(str(html_page), 'html.parser',
                             parse_only=SoupStrainer(TEXTAREA))
    textdata = ''
    if textarea is not None:
        textdata = textarea.text
    return {'data': textdata}


def extract_paste_content(html_page, tz=None):
    r = {}
    r.update(extract_paste_box_line1(html_page))
    r.update(extract_paste_box_line2(html_page, tz=tz))
    r.update(extract_text_data(html_page))
    return r


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
