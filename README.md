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

x = PasteApiBinClient(api_dev_key, api_user_key=api_user_key)
print (x.trends())
print (x.user_pastes(username))

# get first page of search results for key term
c = PasteBinApiClient.paste_search('Hancitor')
# get the paste page for paste key
p = PasteBinApiClient.paste(paste_key)
# Get first page of user pastes
p = PasteBinApiClient.user_pastes(username)
# Get third page of user pastes
p = PasteBinApiClient.user_pastes(username, page=3)
# Get all pages of user pastes
p = PasteBinApiClient.user_pastes(username, do_all=True)
```


## Some Caveats

1. I have only tested this software on Linux, and it will not work in enterprise environments that require HTTP proxies until I add support for proxies.

2. Search is performed using Selenium and headless Chrome, so the request is slow.


