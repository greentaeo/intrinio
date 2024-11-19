from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException
import pandas as pd
import logging
import os

# Intrinio API 키 설정 (환경 변수 사용 권장하지 않고 직접 입력)
api_key = 'OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy'  # 새로운 API 키로 교체하세요
intrinio.ApiClient().set_api_key(api_key)
intrinio.ApiClient().allow_retries(True)

def fetch_company_details(ticker):
    try:
        company = intrinio.CompanyApi().get_company(ticker)
        print(f"Ticker: {company.ticker}")
        print(f"Name: {company.name}")
        print(f"Sector: {getattr(company, 'sector', 'Unknown')}")
        print(f"Market Sector: {getattr(company, 'market_sector', 'Unknown')}")
        print(f"Industry Category: {getattr(company, 'industry_category', 'Unknown')}")
        print(f"Industry Group: {getattr(company, 'industry_group', 'Unknown')}")
    except ApiException as e:
        print(f"API 호출 중 오류 발생: {e}")

# 예시 실행
fetch_company_details('AAPL')  # Apple Inc.
fetch_company_details('BA')    # Boeing Co