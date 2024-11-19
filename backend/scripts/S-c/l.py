from __future__ import print_function
import intrinio_sdk
from intrinio_sdk.rest import ApiException
import datetime
import json
import os
import logging
import re  # 파일 이름 정리를 위한 모듈
import time  # 지연 시간 추가를 위한 모듈

# 1. Intrinio API 키 설정 (보안을 위해 환경 변수 사용 권장)
# 환경 변수 설정 예시 (터미널에서 실행):
# export INTRINIO_API_KEY='YOUR_INTRINIO_API_KEY'

configuration = intrinio_sdk.Configuration()
configuration.api_key['api_key'] = os.getenv('OjI1NDJiNjBlOWY5YTI1NTMzOTZjYzNiODBjNmFmNGNk')  # 환경 변수에서 API 키 가져오기

# API 클라이언트 생성
api_client = intrinio_sdk.ApiClient(configuration)
api_client.configuration.allow_retries = True

# 2. 기업 목록 로드
with open('/Users/xodh3/intrinio/data/all_companies.json', 'r') as f:
    companies_data = json.load(f)

# 기업 식별자 목록 생성 (Intrinsic '_id' 필드 사용)
company_identifiers = []
missing_identifier_companies = []  # 식별자가 없는 기업을 기록하기 위한 리스트

for company in companies_data:
    identifier = company.get('_id')  # '_id' 필드 사용
    if identifier:
        company_identifiers.append(identifier)
    else:
        missing_identifier_companies.append(company)

# 식별자가 없는 기업 로그 기록
if missing_identifier_companies:
    logging.warning(f"식별자가 누락된 기업 수: {len(missing_identifier_companies)}")
    # 식별자가 누락된 기업을 별도의 JSON 파일로 저장
    with open(os.path.join('/Users/xodh3/intrinio/data/collected_data_json', 'missing_identifiers.json'), 'w') as f:
        json.dump(missing_identifier_companies, f, indent=4)

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

# 7. 데이터 저장 경로 설정
data_save_path = '/Users/xodh3/intrinio/data/collected_data_json'
os.makedirs(data_save_path, exist_ok=True)

# 파일 이름에 사용할 수 없는 문자 제거를 위한 함수
def sanitize_filename(name):
    return re.sub(r'[\/:*?"<>|]', '_', name)

# 날짜를 파일 이름에 포함하기 위한 날짜 문자열 생성
date_str = today_date

# 8. 모든 기업의 데이터를 저장할 리스트 초기화
all_companies_data = []

# 기업 데이터를 일정한 배치 크기마다 저장하는 함수
def save_batch_data(batch_number, data):
    file_name = f"All_Companies_Daily_Metrics_{date_str}_batch_{batch_number}.json"
    file_path = os.path.join(data_save_path, file_name)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    logging.info(f"배치 {batch_number}의 데이터를 {file_name} 파일로 저장했습니다.")

# 배치 크기 설정
batch_size = 1000
batch_number = 1

# 9. 각 기업에 대해 각 태그에 대한 데이터 가져오기
for idx, identifier in enumerate(company_identifiers, start=1):
    logging.info(f"({idx}/{len(company_identifiers)}) 기업 데이터 수집 시작: {identifier}")
    try:
        # 기업별 데이터를 저장할 딕셔너리
        company_data = {'company': identifier, 'date': date_str, 'metrics': {}}
        for tag in tags:
            try:
                response = company_api.get_company_historical_data(
                    identifier=identifier,
                    tag=tag,
                    start_date=start_date,
                    end_date=end_date
                )
                if response.historical_data:
                    # 데이터가 있을 경우 metrics 딕셔너리에 추가
                    # 여러 데이터가 있을 경우 첫 번째 데이터만 사용
                    value = response.historical_data[0].value
                    company_data['metrics'][tag] = value
                    logging.info(f"성공: 기업 {identifier}, 태그 {tag}")
                else:
                    # 데이터가 없는 경우 건너뜀
                    pass
                time.sleep(0.1)  # API 호출 제한을 피하기 위해 지연 시간 추가
            except ApiException as e:
                if e.status == 404:
                    # 데이터가 없어서 발생하는 404 에러는 무시하고 로그에 기록하지 않음
                    pass
                else:
                    # 다른 API 예외는 로그에 기록
                    logging.warning(f"API 예외 발생 - 기업 {identifier}, 태그 {tag}: {e}")
            except Exception as e:
                logging.error(f"예상치 못한 오류 - 기업 {identifier}, 태그 {tag}: {e}")

        # 기업의 데이터가 있을 경우 all_companies_data 리스트에 추가
        if company_data['metrics']:
            all_companies_data.append(company_data)
            logging.info(f"기업 {identifier}의 데이터를 수집했습니다.")
        else:
            logging.info(f"기업 {identifier}의 데이터가 없습니다.")

        # 배치 크기마다 데이터를 저장하고 리스트 초기화
        if idx % batch_size == 0:
            save_batch_data(batch_number, all_companies_data)
            all_companies_data = []
            batch_number += 1

    except Exception as e:
        logging.error(f"기업 {identifier}의 데이터 수집 중 오류 발생: {e}")
    logging.info(f"기업 데이터 수집 완료: {identifier}\n")

# 루프 종료 후 남은 데이터 저장
if all_companies_data:
    save_batch_data(batch_number, all_companies_data)

logging.info("모든 데이터 수집이 완료되었습니다.")