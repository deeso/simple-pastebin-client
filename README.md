For the time being usage goes something like this:

``sudo pip3 install -r requirements .``
*$ipython3*

```
from simple_pastebin_client import PasteBinApiClient

api_dev_key = "CREATE" 
api_user_key = "CREATE"

x = PasteApiBinClient(api_dev_key, api_user_key=api_user_key)

print (x.trends())
print (x.user('Matthewm'))

```
