from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')
intrinio.ApiClient().allow_retries(True)

identifier = '$SIC.2911'

response = intrinio.IndexApi().get_sic_index_by_id(identifier)
print(response)
    
# Note: For a Pandas DataFram