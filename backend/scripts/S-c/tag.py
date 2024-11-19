from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException
import datetime
import numpy as np

# Intrinio API 설정
api_client = intrinio.ApiClient()
api_client.configuration.api_key['api_key'] = 'OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy'
api_client.configuration.allow_retries = True

# Company API 인스턴스 생성
company_api = intrinio.CompanyApi(api_client)

def get_historical_data_average(identifier, tag, frequency='daily', years=10):
    """
    주어진 기간(연도 수) 동안의 데이터를 가져와서 평균을 계산하는 함수
    """
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')  # 오늘 날짜
    start_date = (datetime.datetime.now() - datetime.timedelta(days=years*365)).strftime('%Y-%m-%d')  # 10년 전 날짜
    
    try:
        # API 호출
        response = company_api.get_company_historical_data(
            identifier, tag, frequency=frequency, start_date=start_date, end_date=end_date
        )
        
        # 응답 데이터 출력
        print(f"Response for {tag} ({years} years): {response.historical_data}")
        
        # 데이터 값 추출 및 평균 계산
        values = [item.value for item in response.historical_data]
        average_value = np.mean(values) if values else None  # 값이 없으면 None 반환
        return average_value
    
    except ApiException as e:
        print(f"Error fetching historical data for {tag}: {e}")
        return None

def get_averages_for_different_years(identifier, tag, frequency='daily'):
    """
    10년, 7년, 5년, 3년 동안의 평균을 각각 계산하는 함수
    """
    averages = {}
    for years in [10, 7, 5, 3]:
        avg = get_historical_data_average(identifier, tag, frequency=frequency, years=years)
        averages[f"{years}_year_average"] = avg
    return averages

# 요청 파라미터
identifier = 'MSFT'
tags = ['marketcap', ' ' 'debttoequity', 'revenuegrowth']

# frequency 변수 설정
frequency = 'monthly'

# 각 테그에 대해 여러 기간에 대한 평균값 가져오기
for tag in tags:
    averages = get_averages_for_different_years(identifier, tag, frequency=frequency)
    print(f"{tag} averages: {averages}")