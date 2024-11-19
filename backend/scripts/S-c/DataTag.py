from __future__ import print_function
import time
import json
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException
import os

# API 설정
intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')
intrinio.ApiClient().allow_retries(True)

# 경로 설정
save_path = '/Users/xodh3/intrinio/data'
if not os.path.exists(save_path):
    os.makedirs(save_path)

# API 요청 파라미터
tag = ''
type = ''
parent = ''
statement_code = 'income_statement'
fs_template = 'industrial'
page_size = 1000
next_page = ''

try:
    # API 응답
    response = intrinio.DataTagApi().get_all_data_tags(tag=tag, type=type, parent=parent, statement_code=statement_code, fs_template=fs_template, page_size=page_size, next_page=next_page)
    
    # 데이터를 JSON 파일로 저장
    file_name = os.path.join(save_path, 'all.income_statement.json')
    with open(file_name, 'w') as json_file:
        json.dump(response.to_dict(), json_file, indent=4)
    
    print(f"Data tags saved to {file_name}")

except ApiException as e:
    print(f"Error fetching data tags: {e}")