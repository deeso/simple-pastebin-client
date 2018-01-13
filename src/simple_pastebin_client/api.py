from xml.etree.ElementTree import fromstring
from xmljson import parker
import requests
from .consts import *
import tzlocal
import json
from .util import extract_pastes_titles, \
                  extract_paste_content, extract_date_from_html


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

    def raw_user_paste(self, paste_key):
        data = {
                API_OPTION: SHOW_PASTE,
                API_DEV_KEY: self.api_key,
                API_USER_KEY: self.api_user_key,
                API_PASTE_KEY: paste_key
                }
        rsp = requests.post(API_RAW, data=data)
        return rsp.content

    @classmethod
    def raw_paste(self, paste_key):
        url = URL + "/raw/" + paste_key
        rsp = requests.get(url, headers=HEADERS)
        return rsp.content

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
    def user_pastes(cls, username, tz=None):
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

        return cls(api_dev_key, api_user_key=api_user_key,
                   api_user_name=api_user_name,
                   api_user_password=api_user_password,
                   tz_local_name=tz_local_name)
