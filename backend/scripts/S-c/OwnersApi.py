from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')
intrinio.ApiClient().allow_retries(True)

institutional = ''
page_size = 100
next_page = ''

response = intrinio.OwnersApi().get_all_owners(institutional=institutional, page_size=page_size, next_page=next_page)
print(response)
    
