

from __future__ import print_function
import time
from intrinio_sdk import SecurityApi, SecurityScreenGroup, ApiClient
from intrinio_sdk.rest import ApiException

# API 키 설정
ApiClient().set_api_key('OjI1NDJiNjBlOWY5YTI1NTMzOTZjYzNiODBjNmFmNGNk')
ApiClient().allow_retries(True)

# 모든 지표들을 테스트
test_fields = [
    # 성장 지표
    "revenuegrowth", "netincomegrowth", "epsgrowth", "ebitdagrowth", 
    "ebitgrowth", "ocfgrowth", "fcffgrowth",
    
    # 수익성 지표
    "grossmargin", "operatingmargin", "profitmargin", "ebitdamargin",
    "roe", "roa", "roic",
    
    # 유동성 지표
    "currentratio", "quickratio", "nwc",
    
    # 재무 안정성 지표
    "debttoequity", "debttoebitda", "netdebttoebitda", "ltdebttoequity",
    "ebittointerestex", "altmanzscore", "debttototalcapital",
    
    # 효율성 지표
    "assetturnover", "invturnover", "arturnover", "apturnover",
    "faturnover", "investedcapitalturnover",
    
    # 가치 평가 지표
    "pricetoearnings", "pricetobook", "evtoebitda", "pricetorevenue",
    "dividendyield", "enterprisevalue", "earningsyield",
    
    # 현금흐름 지표
    "freecashflow", "ocfgrowth", "capex", "ocftocapex",
    "fcffgrowth", "ocfqoqgrowth", "fcffqoqgrowth"
]

print("=== 지표 지원 여부 테스트 시작 ===\n")

supported_fields = []
unsupported_fields = []

for field in test_fields:
    clauses = [
        {"field": field, "operator": "gt", "value": "0"}
    ]
    
    logic = SecurityScreenGroup(operator="AND", clauses=clauses)
    
    try:
        response = SecurityApi().screen_securities(
            logic=logic,
            order_column='marketcap',
            order_direction='desc',
            primary_only=True,
            page_size=1
        )
        supported_fields.append(field)
        print(f"✓ {field}: 지원됨")
    except ApiException as e:
        unsupported_fields.append(field)
        print(f"✗ {field}: 지원되지 않음")
    
    time.sleep(0.5)  # API 호출 간격

print("\n=== 테스트 결과 요약 ===")
print(f"\n지원되는 지표들 ({len(supported_fields)}):")
for field in supported_fields:
    print(f"- {field}")

print(f"\n지원되지 않는 지표들 ({len(unsupported_fields)}):")
for field in unsupported_fields:
    print(f"- {field}")