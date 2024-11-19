from __future__ import print_function
import time
import json
import os
import datetime
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

# Intrinio API 설정
api_client = intrinio.ApiClient()
api_client.configuration.api_key['api_key'] = 'OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy'
api_client.configuration.allow_retries = True

# Company API 인스턴스 생성
company_api = intrinio.CompanyApi(api_client)

# 기업 목록 로드
company_file_path = '/Users/xodh3/intrinio/data/all_companies.json'
with open(company_file_path, 'r') as f:
    companies_data = json.load(f)

# 테스트를 위해 기업 리스트를 20개로 제한
test_companies_data = companies_data[:20]  # 첫 20개 기업 선택

# 저장 경로 설정 (기업 파일과 동일한 디렉토리)
save_directory = os.path.dirname(company_file_path)
save_file_path = os.path.join(save_directory, 'collected_data.json')

# 사용하려는 태그 리스트 (예시로 20개 태그 설정)
tags = [
    'epsgrowth',
    'revenuegrowth',
    'currentratio',
    'quickratio',
    'assetturnover',
    'invturnover',
    'roe',
    'operatingmargin',
    'pricetoearnings',
    'pricetobook',
    'netmargin',
    'debttoequity',
    'interestcover',
    'dividendyield',
    'pegratio',
    'grossmargin',
    'ebitdamargin',
    'returnonassets',
    'cashratio',
    'workingcapital'
]

# 데이터 수집을 위한 리스트 초기화
collected_data = []

# 시작 시간 기록
start_time = datetime.datetime.now()

# 오류 로그 파일 경로 설정
error_log_file = os.path.join(save_directory, 'error_log.txt')

for company in test_companies_data:
    identifier = company['_id']  # '_id'를 회사 식별자로 사용
    for tag in tags:
        success = False
        while not success:
            try:
                response = company_api.get_company_data_point_number(identifier, tag)
                # 수집된 데이터를 저장
                data_point = {
                    'company_id': identifier,
                    'tag': tag,
                    'value': response
                }
                collected_data.append(data_point)
                print(f"{identifier} - {tag}: {response}")
                success = True  # 성공 시 while 루프 종료
            except ApiException as e:
                if e.status == 429:
                    retry_after = int(e.headers.get('Retry-After', '60'))
                    print(f"Rate limit exceeded. Sleeping for {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    error_message = f"Error fetching {identifier} - {tag}: {e}"
                    print(error_message)
                    with open(error_log_file, 'a') as log_file:
                        log_file.write(error_message + '\n')
                    success = True  # 다른 오류의 경우에는 다음으로 넘어감
            except Exception as e:
                error_message = f"Unexpected error fetching {identifier} - {tag}: {e}"
                print(error_message)
                with open(error_log_file, 'a') as log_file:
                    log_file.write(error_message + '\n')
                success = True

# 종료 시간 기록 및 총 소요 시간 계산
end_time = datetime.datetime.now()
elapsed_time = end_time - start_time
print(f"Total elapsed time: {elapsed_time}")

# 수집된 데이터를 저장 경로에 JSON 파일로 저장
with open(save_file_path, 'w') as outfile:
    json.dump(collected_data, outfile)