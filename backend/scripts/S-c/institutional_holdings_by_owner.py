from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

# Intrinio API 키 설정
intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')
intrinio.ApiClient().allow_retries(True)

# 오너 식별자 리스트 업데이트
owner_identifiers = ['0000001800', '0000001961', '0000002110', '0000002230']
page_size = 100
as_of_date = '2023-01-05'
next_page = ''

# 각 오너에 대한 데이터 가져오기
for identifier in owner_identifiers:
    try:
        response = intrinio.OwnersApi().institutional_holdings_by_owner(
            identifier, 
            page_size=page_size, 
            as_of_date=as_of_date, 
            next_page=next_page
        )
        print(f"Data for owner CIK {identifier}:")
        print(response)
    except ApiException as e:
        print(f"Exception when calling OwnersApi for owner CIK {identifier}: {e}\n")