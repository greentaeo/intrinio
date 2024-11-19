from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException
import pandas as pd

# Intrinio API 키 설정
intrinio.ApiClient().set_api_key('OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy')  # 자신의 API 키로 대체하세요
intrinio.ApiClient().allow_retries(True)

def get_company_details(ticker):
    try:
        # get_company 메서드 사용 (티커 기반)
        company_info = intrinio.CompanyApi().get_company(ticker)
        
        # 회사 정보 확인
        company_data = {
            'id': company_info.id,
            'ticker': company_info.ticker,
            'name': company_info.name,
            'lei': company_info.lei,
            'legal_name': company_info.legal_name,
            'stock_exchange': company_info.stock_exchange,
            'sic': company_info.sic,
            'short_description': company_info.short_description,
            'long_description': company_info.long_description,
            'ceo': company_info.ceo,
            'company_url': company_info.company_url,
            'business_address': company_info.business_address,
            'mailing_address': company_info.mailing_address,
            'business_phone_no': company_info.business_phone_no,
            'hq_address1': company_info.hq_address1,
            'hq_address2': company_info.hq_address2,
            'hq_address_city': company_info.hq_address_city,
            'hq_address_postal_code': company_info.hq_address_postal_code,
            'entity_legal_form': company_info.entity_legal_form,
            'cik': company_info.cik,
            'latest_filing_date': company_info.latest_filing_date,
            'hq_state': company_info.hq_state,
            'hq_country': company_info.hq_country,
            'inc_state': company_info.inc_state,
            'inc_country': company_info.inc_country,
            'employees': company_info.employees,
            'entity_status': company_info.entity_status,
            'sector': company_info.sector,
            'industry_category': company_info.industry_category,
            'industry_group': company_info.industry_group,
            'template': company_info.template,
            'standardized_active': company_info.standardized_active,
            'first_fundamental_date': company_info.first_fundamental_date,
            'last_fundamental_date': company_info.last_fundamental_date,
            'first_stock_price_date': company_info.first_stock_price_date,
            'last_stock_price_date': company_info.last_stock_price_date
        }
        
        return company_data
    
    except ApiException as e:
        print(f"API 호출 중 오류 발생 ({ticker}): {e}")
        return None

def main():
    # 조회하고자 하는 회사의 티커 리스트
    tickers = ['INTC', 'WMT', 'MSFT', 'IBM', 'GM', 'FDX', 'TMO', 'HAL', 'V', 'KO']
    
    # 결과를 저장할 리스트 초기화
    detailed_companies = []
    
    for ticker in tickers:
        print(f"{ticker}의 상세 정보를 가져오는 중...")
        company_data = get_company_details(ticker)
        if company_data:
            detailed_companies.append(company_data)
            print(f"{ticker}의 정보가 성공적으로 추가되었습니다.")
        else:
            print(f"{ticker}의 정보를 가져오는 데 실패했습니다.")
        time.sleep(0.5)  # Rate Limiting 방지
    
    # 데이터프레임 생성
    df = pd.DataFrame(detailed_companies)
    
    # 결과 저장
    df.to_excel('individual_companies_with_sector.xlsx', index=False)
    print("개별 기업 데이터와 섹터 정보가 'individual_companies_with_sector.xlsx' 파일로 저장되었습니다.")

if __name__ == "__main__":
    main()