from xml.etree.ElementTree import fromstring
from bs4 import BeautifulSoup, SoupStrainer
from xmljson import parker
import requests
from .consts import *
import tzlocal
import json
from .util import has_attr, extract_date, extract_pastes_titles, \
                  extract_paste_content


class PasteBinApiClient(object):
    TZ = tzlocal.get_localzone().zone
    KEY = 'pastebin-api-client'

    def __init__(self, api_key, api_user_key=None,
                 api_user_name=None, api_user_password=None,
                 tz_local_name=TZ):
        self.api_key = api_key
        self.api_user_key = api_user_key
        self.tz = tz_local_name

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

    def raw(self, paste_key):
        data = {
                API_OPTION: SHOW_PASTE,
                API_DEV_KEY: self.api_key,
                API_USER_KEY: self.api_user_key,
                API_PASTE_KEY: paste_key
                }
        rsp = requests.post(API_RAW, data=data)
        return rsp.content

    def paste_raw(self, paste_key):
        url = URL + "/raw/" + paste_key
        rsp = requests.get(url, headers=HEADERS)
        return rsp.content

    def paste(self, paste_key):
        return extract_paste_content(self.paste_html(paste_key), self.tz)

    def paste_html(self, paste_key):
        url = URL + "/" + paste_key
        rsp = requests.post(url, headers=HEADERS)
        return rsp.content

    def paste_date(self, paste_key, html_page=None,
                   tz=None, tz_conversion=None):
        tz = self.tz if tz is None else tz
        if html_page is None:
            html_page = self.paste(paste_key)

        _span = BeautifulSoup(html_page, 'html.parser',
                              parse_only=SoupStrainer('span'))
        spans = [i for i in _span.find_all() if has_attr(i, 'title')]
        if len(spans) == 1:
            if tz_conversion is not None:
                tz = tz_conversion(spans[0]['title'])
                tz = self.tz if tz is None else tz
            return extract_date(spans[0]['title'], tz=tz)
        else:
            # TODO fixme this is bad
            for s in spans:
                try:
                    if tz_conversion is not None:
                        tz = tz_conversion(s)
                        tz = self.tz if tz is None else tz
                    return extract_date(s, tz=tz)
                except:
                    pass
        return None

    def user_pastes(self, username, tz_conversion=None):
        results = []
        url = URL_USER.format(**{'user': username})
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # client = webdriver.Chrome(chrome_options=options)
        # client.get(url)
        rsp = requests.get(url, headers=HEADERS)
        data = rsp.text
        pastes_titles = extract_pastes_titles(data)
        for p, t in pastes_titles:
            pdata = self.paste_raw(p)
            date = self.paste_date(p, tz_conversion=tz_conversion)
            purl = URL + '/{}'.format(p)
            results.append({'data': pdata,
                            'title': t,
                            'paste': purl,
                            'date': date})
        return results

    def xml_to_json(self, data):
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

        return cls(api_dev_key, api_user_key=api_user_key,
                   api_user_name=api_user_name,
                   api_user_password=api_user_password,
                   tz_local_name=tz_local_name)
