from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')
intrinio.ApiClient().allow_retries(True)

page_size = 10000
next_page = ''

response = intrinio.IndexApi().get_all_economic_indices(page_size=page_size, next_page=next_page)
print(response)
    
