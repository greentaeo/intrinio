

from __future__ import print_function
import intrinio_sdk
from intrinio_sdk.rest import ApiException
import datetime
import json
import os
import logging

# 1. Intrinio API 키 설정
configuration = intrinio_sdk.Configuration()
configuration.api_key['api_key'] = 'OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy'  # 여기에 API 키를 직접 입력하세요

# API 클라이언트 생성
api_client = intrinio_sdk.ApiClient(configuration)
api_client.configuration.allow_retries = True

# 2. 기업 목록 로드
with open('/Users/xodh3/intrinio/data/all_companies.json', 'r') as f:
    companies_data = json.load(f)

# 기업 식별자 목록 생성 (_ticker 또는 다른 고유 식별자를 사용)
company_identifiers = [company['_ticker'] for company in companies_data]

# 3. 태그(지표) 목록 로드
with open('/Users/xodh3/intrinio/data/tags.json', 'r') as f:
    tags_data = json.load(f)

# 태그 목록 생성
tags = [metric['tag'] for metric in tags_data['metrics']]

# 4. 날짜 설정 (시작 날짜와 종료 날짜를 모두 오늘 날짜로 설정)
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
start_date = today_date
end_date = today_date

# 5. API 인스턴스 생성
company_api = intrinio_sdk.CompanyApi(api_client)

# 6. 로그 설정
logging.basicConfig(
    filename='data_fetch.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# 7. 각 기업에 대해 각 태그에 대한 데이터 가져오기
for identifier in company_identifiers:
    logging.info(f"기업 데이터 수집 시작: {identifier}")
    for tag in tags:
        try:
            response = company_api.get_company_historical_data(
                identifier,
                tag,
                start_date=start_date,
                end_date=end_date
            )
            # 데이터 출력 또는 저장
            logging.info(f"성공: 기업 {identifier}, 태그 {tag}")
            # 필요한 경우 데이터를 파일이나 데이터베이스에 저장할 수 있습니다.
        except ApiException as e:
            logging.warning(f"API 예외 발생 - 기업 {identifier}, 태그 {tag}: {e}")
            # 오류가 발생해도 다음 태그로 넘어갑니다.
        except Exception as e:
            logging.error(f"예상치 못한 오류 - 기업 {identifier}, 태그 {tag}: {e}")
            # 오류가 발생해도 다음 태그로 넘어갑니다.
    logging.info(f"기업 데이터 수집 완료: {identifier}\n")

logging.info("모든 데이터 수집이 완료되었습니다.")