from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')
intrinio.ApiClient().allow_retries(True)

query = 'Apple'
active = True
mode = ''
page_size = 100

response = intrinio.CompanyApi().search_companies(query, active=active, mode=mode, page_size=page_size)
print(response)
    
