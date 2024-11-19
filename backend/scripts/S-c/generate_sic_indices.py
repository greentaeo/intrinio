from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException
import pandas as pd
import re

# API 클라이언트 설정
intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')  # 자신의 API 키로 대체하세요
intrinio.ApiCli



ent().allow_retries(True)

# 페이지 사이즈 설정
page_size = 100
next_page = ''

# 모든 심볼과 추가 정보를 저장할 리스트
all_data = []

# next_page가 없을 때까지 데이터를 계속 가져옴
while True:
    try:
        response = intrinio.IndexApi().get_all_sic_indices(page_size=page_size, next_page=next_page)
        
        # 각 항목에서 필요한 정보를 추출하여 딕셔너리로 저장
        for item in response.indices:
            # symbol에서 SIC 코드 숫자 부분 추출
            code_match = re.search(r'\d+', item.symbol)
            if code_match:
                code = code_match.group()
            else:
                code = 'Unknown'

            data = {
                'Symbol': item.symbol,
                'Name': item.name,
                'Code': code,
                'Country': item.country
            }
            all_data.append(data)
        
        # 다음 페이지가 없으면 루프 종료
        if not response.next_page:
            break
        next_page = response.next_page
    
    except ApiException as e:
        print("API 호출 중 오류 발생: %s\n" % e)
        break

# 데이터프레임 생성
df = pd.DataFrame(all_data)

# 엑셀 파일로 저장
df.to_excel('sic_indices.xlsx', index=False)

print("데이터가 'sic_indices.xlsx' 파일로 저장되었습니다.")



