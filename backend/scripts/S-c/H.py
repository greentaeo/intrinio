from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')
intrinio.ApiClient().allow_retries(True)

clauses = [
  {
    "field": "marketcap",
    "operator": "gt",
    "value": "10000000"
  },
  {
    "field": "beta",
    "operator": "lt",
    "value": "5"
  }
]

logic = intrinio.SecurityScreenGroup(operator="AND", clauses=clauses)
order_column = 'marketcap'
order_direction = 'asc'
primary_only = False
page_size = 100

response = intrinio.SecurityApi().screen_securities(logic=logic, order_column=order_column, order_direction=order_direction, primary_only=primary_only, page_size=page_size)
print(response)
    
