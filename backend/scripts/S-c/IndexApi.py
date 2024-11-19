from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

# API 클라이언트 설정
intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')
intrinio.ApiClient().allow_retries(True)

# 페이지 사이즈 설정
page_size = 100
next_page = ''

# 모든 심볼을 저장할 리스트
all_symbols = []

# next_page가 없을 때까지 데이터를 계속 가져옴
while True:
    response = intrinio.IndexApi().get_all_sic_indices(page_size=page_size, next_page=next_page)
    symbols = [item.symbol for item in response.indices]
    all_symbols.extend(symbols)
    
    # 다음 페이지가 없으면 루프 종료
    if not response.next_page:
        break
    next_page = response.next_page

# 모든 심볼 출력 및 총 개수 출력
print(f"Symbols: {all_symbols}")
print(f"Total number of symbols: {len(all_symbols)}")

