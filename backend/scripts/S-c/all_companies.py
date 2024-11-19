import os
import json
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

intrinio.ApiClient().set_api_key('OjI1NDJiNjBlOWY5YTI1NTMzOTZjYzNiODBjNmFmNGNk')
intrinio.ApiClient().allow_retries(True)

#저장할 디렉토리 설정
save_path = '/Users/xodh3/intrinio'
os.makedirs(save_path, exist_ok=True)  # 디렉토리가 없으면 생성

# 필터링 조건 초기화
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

# 기업 정보를 저장할 리스트
all_companies = []

while True:
    try:
        # API 호출
        response = intrinio.CompanyApi().get_all_companies(
            latest_filing_date=latest_filing_date,
            sic=sic,
            template=template,
            sector=sector,
            industry_category=industry_category,
            industry_group=industry_group,
            has_fundamentals=has_fundamentals,
            has_stock_prices=has_stock_prices,
            thea_enabled=thea_enabled,
            page_size=page_size,
            next_page=next_page
        )
        
        # 응답에서 모든 기업 정보를 리스트에 추가
        all_companies.extend([company.__dict__ for company in response.companies])

        # 다음 페이지가 있는지 확인
        next_page = response.next_page
        if not next_page:  # 더 이상 페이지가 없으면 종료
            break

    except ApiException as e:
        print(f"API 호출 오류: {e}")
        break

# 모든 기업 정보를 JSON 파일로 저장
output_file = os.path.join(save_path, 'all_companies.json')
with open(output_file, 'w') as f:
    json.dump(all_companies, f, indent=4)

print(f"총 기업 수: {len(all_companies)}")
print(f"기업 정보가 파일에 저장되었습니다: {output_file}")