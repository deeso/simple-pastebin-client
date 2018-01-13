from selenium import webdriver
from xml.etree.ElementTree import fromstring
from xmljson import parker
import requests
from .consts import *
import tzlocal
import json
import urllib
from googleapiclient.discovery import build
from .util import extract_pastes_titles, extract_elements, \
                  extract_paste_content, extract_date_from_html


class PasteBinApiClient(object):
    TZ = tzlocal.get_localzone().zone
    KEY = 'pastebin-api-client'

    def __init__(self, api_key, api_user_key=None,
                 api_user_name=None, api_user_password=None,
                 tz_local_name=TZ, search_api=None,
                 key=None, sig=None, cse_cx=None, cse_tok=None):
        self.api_key = api_key
        self.api_user_key = api_user_key
        self.tz = tz_local_name
        self.search_api = search_api_key
        self.key = key
        self.sig = sig
        self.cse_cx = cse_cx
        self.query = query
        self.cse_tok = cse_tok
        if api_user_password is not None and \
           api_user_name is not None:
            self.api_user_key = self.login(api_user_name, api_user_password)

    def login(self, api_user_name, api_user_password):
        data = {
                API_DEV_KEY: self.api_key,
                API_USER_NAME: api_user_name,
                API_USER_PASSWORD: api_user_password
                }
        rsp = requests.post(API_LOGIN, data=data, headers=HEADERS)
        data = rsp.text
        e = [
             INVALIDE_REQUEST, INVALID_API_KEY,
             INVALID_LOGIN, ACCOUNT_NOT_ACTIVE,
             INVALID_PARAMS,
             ]
        if data in e:
            raise Exception(data)
        return data

    def list(self, user_key, limit=100):
        data = {
                API_OPTION: LIST,
                API_DEV_KEY: self.api_key,
                LIMIT: limit,
                API_USER_KEY: user_key
                }
        rsp = requests.post(API_POST, data=data, headers=HEADERS)
        return rsp

    def trends(self):
        data = {
                API_OPTION: TRENDS,
                API_DEV_KEY: self.api_key
                }
        rsp = requests.post(API_POST, data=data, headers=HEADERS)
        data = (rsp.text).strip()
        if data.find("<paste>") == 0:
            w = "<pastes>{}</pastes>".format(data)
            return self.xml_to_json(w)
        raise Exception(data)

    def raw_user_paste(self, paste_key):
        data = {
                API_OPTION: SHOW_PASTE,
                API_DEV_KEY: self.api_key,
                API_USER_KEY: self.api_user_key,
                API_PASTE_KEY: paste_key
                }
        rsp = requests.post(API_RAW, data=data)
        return rsp.content

    def search(self, query):
        if self.search_api_key is None:
            return None
        service = build("customsearch", "v1",
                        developerKey=self.search_api_key)
        q = urllib.parse.quote_plus(query)
        res = service.cse().list(
              q=q,
              cx='013305635491195529773:0ufpuq-fpt0',
              sort='date',
              num=20,
            ).execute()
        return res

    @classmethod
    def raw_paste(self, paste_key):
        url = URL + "/raw/" + paste_key
        rsp = requests.get(url, headers=HEADERS)
        return rsp.content

    @classmethod
    def paste_search(cls, query, key=None, sig=None,
                     cse_cx=None, cse_tok=None):
        q = urllib.parse.quote_plus(query)
        url = URL_SEARCH.format(**{'query': q})
        do_ex = False
        if key is not None and \
           sig is not None and \
           cse_cx is not None and \
           cse_tok is not None:
            do_ex = True
            values = {
                'key': key,
                'sig': sig,
                'cse_cx': cse_cx,
                'cse_tok': cse_tok,
                'query': q,
            }
            url = CSE_QUERY.format(**values)

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        client = webdriver.Chrome(chrome_options=options)
        client.get(url)
        while len(client.page_source) < 1000:
            client.get(url)

        html_source = client.page_source
        results = []
        if len(html_source) > 1000 and not do_ex:
            hrefs = extract_elements(html_source, 'a', 'data-ctorig')
            for href in hrefs:
                byline = href.next_sibling.text
                paste = href.get('data-ctorig', None)
                pk = None if paste is None else paste.split('/')[-1]
                results.append({'paste': paste,
                                'pastekey': pk,
                                'byline': byline})

        elif len(html_source) > 1000 and not do_ex:
            return html_source
        return results

    def ipaste_search(self, query):
        return cls.paste_search(query, key=self.key, sig=self.sig,
                                cse_cx=self.cse_cx,
                                cse_tok=self.cse_tok)

    @classmethod
    def paste(cls, paste_key, get_raw=True, tz=TZ):
        url = URL + "/raw/" + paste_key
        info = extract_paste_content(cls.paste_html(paste_key), tz)
        info['paste'] = url
        if get_raw:
            info['data'] = cls.raw_paste(paste_key)
        return info

    @classmethod
    def paste_html(cls, paste_key):
        url = URL + "/" + paste_key
        rsp = requests.post(url, headers=HEADERS)
        return rsp.content

    @classmethod
    def paste_date(self, paste_key, html_page=None, tz=None):
        tz = self.tz if tz is None else tz
        if html_page is None:
            html_page = self.paste_html(paste_key)
        return extract_date_from_html(html_page, tz=tz)

    @classmethod
    def user_pastes(cls, username, page=1, tz=None):
        results = []
        url = URL_USER.format(**{'user': username,
                              'page': page})
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # client = webdriver.Chrome(chrome_options=options)
        # client.get(url)
        rsp = requests.get(url, headers=HEADERS)
        data = rsp.text
        pastes_titles = extract_pastes_titles(data)
        for p, t in pastes_titles:
            info = cls.paste(p, get_raw=True)
            results.append(info)
        return results

    @classmethod
    def xml_to_json(cls, data):
        s = json.dumps(parker.data(fromstring(data)))
        # TODO FIXME this is a hack
        if len(json.loads(s).values()) > 0:
            return list(json.loads(s).values())[0]
        return []

    @classmethod
    def parse_toml_file(cls, toml_file):
        return cls.parse_toml(toml.load(open(toml_file)))

    @classmethod
    def parse_toml(cls, toml_dict):
        block = toml_dict.get('pastebin-api-client', toml_dict)
        bt = block.get('type', None)
        if bt is None or bt != 'pastebin-api-client':
            raise Exception("Type is not properly defined")

        api_dev_key = block.get('api_dev_key', None)
        api_user_key = block.get('api_user_key', None)
        api_user_name = block.get('api_user_name', None)
        api_user_password = block.get('api_user_password', None)
        tz_local_name = block.get('tz_local_name', None)

        key = block.get('key', None)
        sig = block.get('sig', None)
        cse_cx = block.get('cse_cx', None)
        cse_tok = block.get('cse_tok', None)

        return cls(api_dev_key, api_user_key=api_user_key,
                   api_user_name=api_user_name,
                   api_user_password=api_user_password,
                   tz_local_name=tz_local_name, key=key,
                   sig=sig, cse_cx=cse_cx, cse_tok=cse_tok)
