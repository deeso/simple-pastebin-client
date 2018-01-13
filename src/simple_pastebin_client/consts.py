DATA_SOURCES = {}
NAME = 'simple-pastebin-scraper'
LOGGER = None
LOGGING_FORMAT = '[%(asctime)s - %(name)s] %(message)s'

# urls
URL = "https://pastebin.com"
URL_USER = "https://pastebin.com/u/{user}/{page}/0/1/?o=a1"
URL_RAW = "https://pastebin.com/raw/{raw}"
URL_SEARCH = "https://pastebin.com/search?q={query}"
API_POST = "https://pastebin.com/api/api_post.php"
API_LOGIN = "https://pastebin.com/api/api_login.php"
API_RAW = "https://pastebin.com/api/api_raw.php"


LIMIT = "limit"
TRENDS = "trends"
LIST = "list"
SHOW_PASTE = "show_paste"

API_PASTE_KEY = 'api_paste_key'
API_USER_NAME = "api_user_name"
API_USER_PASSWORD = "api_user_password"
API_DEV_KEY = "api_dev_key"
API_USER_KEY = "api_user_key"
API_OPTION = "api_option"


INVALIDE_REQUEST = "Bad API request, use POST request, not GET"
INVALID_API_KEY = "Bad API request, invalid api_dev_key"
INVALID_LOGIN = "Bad API request, invalid login"
ACCOUNT_NOT_ACTIVE = "Bad API request, account not active"
INVALID_PARAMS = "Bad API request, invalid POST parameters"

LIST_POST_FMT = "api_option=list&api_dev_key={API_KEY}" + \
                "&api_user_key={USER_KEY}&api_results_limit={LIMIT}"

TRENDS_POST_FMT = "api_option=trends&api_dev_key={API_KEY}"

MFF = 'Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0'
HEADERS = {'User-Agent': MFF}

EXPECTED_PB_TIME = "%A %d %B %Y  %H:%M:%S %p %Z"

DIV = 'div'
CLASS = 'class'
PBOX_1 = 'paste_box_line1'
PBOX_2 = 'paste_box_line2'
TEXTAREA = 'textarea'


CSE_QUERY = "https://www.googleapis.com/customsearch/v1element?{key}&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig={sig}&cx={cse_cx}&q={query}&cse_tok={cse_tok}&sort=date&googlehost=www.google.com&callback=google.search.Search.apiary9150"