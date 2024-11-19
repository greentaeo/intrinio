from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')
intrinio.ApiClient().allow_retries(True)

latest_filing_date = ''
sic = ''
template = ''
sector = ''
industry_category = ''
industry_group = ''
has_fundamentals = True
has_stock_prices = True
thea_enabled = ''
page_size = 100
next_page = ''

response = intrinio.CompanyApi().get_all_companies(latest_filing_date=latest_filing_date, sic=sic, template=template, sector=sector, industry_category=industry_category, industry_group=industry_group, has_fundamentals=has_fundamentals, has_stock_prices=has_stock_prices, thea_enabled=thea_enabled, page_size=page_size, next_page=next_page)
print(response)
    
    