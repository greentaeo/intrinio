from __future__ import print_function
import os
import json  # json 모듈 임포트 추가
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException
import time

# API 키 설정
intrinio.ApiClient().set_api_key('OjI1NDJiNjBlOWY5YTI1NTMzOTZjYzNiODBjNmFmNGNk')
intrinio.ApiClient().allow_retries(True)

# 데이터 저장 경로 설정
data_path = '/Users/xodh3/intrinio/data/all_companies.json'

# JSON 파일에서 기업 정보를 불러오기
with open(data_path, 'r') as f:
    companies = json.load(f)

# 모든 서류 정보를 저장할 리스트
all_filings = []

# 각 기업에 대해 서류 가져오기
for company in companies:
    company_name = company['_name']  # 기업 이름 가져오기
    company_id = company['_id']  # 고유 ID 가져오기

    report_type = ''  # 모든 보고서 타입 요청
    start_date = '2010-01-01'
    end_date = ''
    industry_category = ''
    industry_group = ''
    thea_enabled = ''
    page_size = 100
    next_page = ''

    while True:
        try:
            print(f"Fetching filings for company: {company_name}")  # 상태 메시지 출력

            # API 호출: 각 기업의 서류 가져오기
            response = intrinio.FilingApi().get_all_filings(
                company=company_id,  # 고유 ID를 API 호출에 사용
                report_type=report_type,
                start_date=start_date,
                end_date=end_date,
                industry_category=industry_category,
                industry_group=industry_group,
                thea_enabled=thea_enabled,
                page_size=page_size,
                next_page=next_page
            )
            
            # 서류 정보를 리스트에 추가 (고유 ID는 포함하지 않음)
            for filing in response.filings:
                filing_data = filing.to_dict()  # Filing 객체를 딕셔너리로 변환
                filing_data['company_name'] = company_name  # 기업 이름만 추가
                all_filings.append(filing_data)

            # 상태 메시지 출력
            print(f"Successfully fetched {len(response.filings)} filings for {company_name}")

            # 다음 페이지가 있는지 확인
            next_page = response.next_page
            if not next_page:  # 더 이상 페이지가 없으면 종료
                break
        except ApiException as e:
            print(f"Error fetching data for company {company_name}: {e}")
            break

# 모든 서류 정보를 JSON 파일로 저장
output_file = os.path.join('/Users/xodh3/intrinio/data', 'all_filings.json')
with open(output_file, 'w') as f:
    json.dump(all_filings, f, indent=4)

print(f"총 서류 수: {len(all_filings)}")
print(f"모든 서류 정보가 파일에 저장되었습니다: {output_file}")