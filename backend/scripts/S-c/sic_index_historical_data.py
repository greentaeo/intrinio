from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')
intrinio.ApiClient().allow_retries(True)

identifier = '$SIC.1'
tag = 'marketcap'
type = ''
start_date = '2018-01-01'
end_date = ''
sort_order = 'desc'
page_size = 100
next_page = ''

response = intrinio.IndexApi().get_sic_index_historical_data(identifier, tag, type=type, start_date=start_date, end_date=end_date, sort_order=sort_order, page_size=page_size, next_page=next_page)
print(response)
    
