from __future__ import print_function
import time
import json
import os
import datetime
import scripts.sic as sic  # 우리가 만든 모듈을 import

# 기업 목록 로드
company_file_path = '/Users/xodh3/intrinio/data/all_companies.json'
with open(company_file_path, 'r') as f:
    companies_data = json.load(f)

# 테스트를 위해 기업 리스트를 20개로 제한
test_companies_data = companies_data[:20]  # 첫 20개 기업 선택

# 저장 경로 설정 (기업 파일과 동일한 디렉토리)
save_directory = os.path.dirname(company_file_path)
save_file_path = os.path.join(save_directory, 'collected_data.json')

# 오류 로그 파일 경로 설정
error_log_file = os.path.join(save_directory, 'error_log.txt')

# 시작 시간 기록
start_time = datetime.datetime.now()

# 지표 태그 가져오기
indicator_tags = sic.get_indicator_tags()

# 데이터 수집 실행
collected_data = sic.collect_data(test_companies_data, indicator_tags, error_log_file)

# 종료 시간 기록 및 총 소요 시간 계산
end_time = datetime.datetime.now()
elapsed_time = end_time - start_time
print(f"Total elapsed time: {elapsed_time}")

# 수집된 데이터를 저장 경로에 JSON 파일로 저장
with open(save_file_path, 'w') as outfile:
    json.dump(collected_data, outfile)