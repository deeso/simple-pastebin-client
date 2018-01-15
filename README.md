## Simple Pastebin Client
**simple-pastebin-client** is a functional Python package that provides programatic *read* access to Pastebin.  This Python package will leverage both the Pastebin API and HTML produced by the service.  While its not a complete implementation of the Pastebin API it does offer the following benefits:

1. Search for pastes by keyword using Selenium's Chrome Headless driver
2. Get a page of pastes or all pastes for a particular user
3. Return content in a JSON format

## Usage

For the time being usage goes something like this:

``sudo pip3 install -r requirements .``
**$ipython3**

```
from simple_pastebin_client import PasteBinApiClient

api_dev_key = "CREATE" 
api_user_key = "CREATE"

# using the published API for some stuff
x = PasteApiBinClient(api_dev_key, api_user_key=api_user_key)
print (x.trends())
print (x.user_pastes(username))

# using HTML scraping for other stuff
# get first page of search results for key term
c = PasteBinApiClient.paste_search('Hancitor')
print (c)
[{'paste': 'https://pastebin.com/Jye4AMsH',
  'byline': 'Some love from man1/hancitor group Today send-safe: from: http ...',
  'pastekey': 'Jye4AMsH'},...
]

# get the paste page for paste key
paste_keys = [i['paste_key'] for i in c]
paste_key = paste_keys[-1] 

p = PasteBinApiClient.paste(paste_key)
print (p)
{'timestamp': '2017-08-21T15:56:06Z',
 'user': '...',
 'data': b'...',
 'unix': 1503348966,
 'paste': 'https://pastebin.com/raw/...',
 'title': '8/21/17 Hancitor'}

# find some like minded users using the search results
interesting_users = set()
for i in c:
    paste_key = i['paste_key']
    p = PasteBinApiClient.paste(paste_key)
    interesting_users.add(p['user'])

print ([i for i in interesting_users if len(i) > 0])

user = [i for i in interesting_users if len(i) > 0][-1]

# Get first page of user pastes
u = PasteBinApiClient.user_pastes(user)
print (len(u), '\n', u)
100
[{'expiration': 'Never',
  'paste_key': '...',
  'title': 'Untitled',
  'unix': 1515931200,
  'syntax': 'None',
  'paste': 'https://pastebin.com/...',
  'hits': '53'},
 {'expiration': 'Never',
  'paste_key': '...',
  'title': 'Untitled',
  'unix': 1515758400,
  'syntax': 'None',
  'paste': 'https://pastebin.com/...',
  'hits': '...'}, ...
]

#Get all the pages of pastes *and* data from the user's profile
u = PasteBinApiClient.user_pastes_data(user, do_all=do_all)
print (len(u), '\n', u)
500
{'data': b'...',
 'syntax': 'None',
 'expiration': 'Never',
 'hits': '...',
 'paste': 'https://pastebin.com/raw/...',
 'user': '...',
 'unix': 1504645473,
 'paste_key': '...',
 'title': '...',
 'timestamp': '2017-09-05T16:04:33Z'}

# get the last page pastes and raw data in the users profile
last_page = PasteBinApiClient.user_pastes_pages(user)
u = PasteBinApiClient.user_pastes_data(user, page=last_page)


# practical use case
interesting_users = set()
query_terms = [
    'adwind malware',
    'adylkuzz malware',
    'alphacrypt malware',
    'andromeda malware',
    'angler malware',
    'asprox malware',
    'backoff malware',
    'bamital malware',
    'banjori malware',
    'bebloh malware',
    'bedep malware',
    'beebone malware',
    'blackenergy malware',
    'brobot malware',
    'caphaw malware',
    'carbanak malware',
    'cerber malware',
    'conficker malware',
    'corebot malware',
    'cryptxxx malware',
    'cryptodefense malware',
    'cryptolocker malware',
    'cryptominer malware',
    'cryptowall malware',
    'darkleech malware',
    'dexter malware',
    'dircrypt malware',
    'dridex malware',
    'dyre malware',
    'eitest malware',
    'emotet malware',
    'explosive malware',
    'fiesta malware',
    'fobber malware',
    'formbook malware',
    'gameover zeus malware',
    'geodo malware',
    'globeimposter malware',
    'hailstorm malware',
    'hancitor malware',
    'havex malware',
    'hesperbot malware',
    'icedid malware',
    'infinity malware',
    'kelihos malware',
    'kraken malware',
    'kuluoz malware',
    'locky malware',
    'magnitude malware',
    'mask malware',
    'matsnu malware',
    'mirai malware',
    'murofet malware',
    'necurs malware',
    'neutrino malware',
    'nuclear malware',
    'nyetya malware',
    'odin malware',
    'padcrypt malware',
    'petya malware',
    'pony malware',
    'pushdo malware',
    'pykspa malware',
    'qadars malware',
    'qakbot malware',
    'ramdo malware',
    'ramnit malware',
    'ranbyus malware',
    'reign malware',
    'rig malware',
    'rovnix malware',
    'shiotob malware',
    'sisron malware',
    'sofacy malware',
    'sundown malware',
    'suppobox malware',
    'sweetorange malware',
    'symmi malware',
    'tempedreve malware',
    'terdot malware',
    'teslacrypt malware',
    'tinba malware',
    'torrentlocker malware',
    'trickbot malware',
    'upatre malware',
    'vawtrak malware',
    'wannacry malware',
    'webcryptominer malware',
    'wirelurker malware',
    'x-agent malware',
    'xpiro malware',
    'zbot malware',
    'zepto malware',
]

for qt in query_terms:
    c = PasteBinApiClient.paste_search(qt)
    for i in c:
        pastekey = i['paste_key']
        p = PasteBinApiClient.paste(pastekey)
        if len(p['user']) > 0:
            interesting_users.add(p['user'])

print ("Interesting Pastebin Users")
for user in sorted(interesting_users):
    print ("https://pastebin.com/u/"+user)


```


## Some Caveats

1. I have only tested this software on Linux, and it will not work in enterprise environments that require HTTP proxies until I add support for proxies.

2. Search is performed using Selenium and headless Chrome, so the request is slow.  Search is also limited because Pastebin proxies queries to Google Custom Search service, which is why a brower is needed to render the pages.  
  
3. If you plan to use the search function, you'll need to install the Chrome drivers for the Selenium package.  I have included a script to help with this in the **configs** directory of the project. 

4. Tests were done by hand, because this was a small weekend project.  If this project matures, I'll add more formal testing. 

