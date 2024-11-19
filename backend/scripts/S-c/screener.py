from __future__ import print_function
import time
from intrinio_sdk import SecurityApi, SecurityScreenGroup, ApiClient
from intrinio_sdk.rest import ApiException

# API 키 설정
ApiClient().set_api_key('OjI1NDJiNjBlOWY5YTI1NTMzOTZjYzNiODBjNmFmNGNk')
ApiClient().allow_retries(True)


clauses = [
    # 성장 지표 (4개)
    {"field": "revenuegrowth", "operator": "gt", "value": "10"},        # 매출 성장률
    {"field": "netincomegrowth", "operator": "gt", "value": "5"},       # 순이익 성장률
    {"field": "epsgrowth", "operator": "gt", "value": "5"},             # EPS 성장률
    {"field": "fcffgrowth", "operator": "gt", "value": "5"},            # 잉여현금흐름 성장률

    # 수익성 지표 (4개)
    {"field": "grossmargin", "operator": "gt", "value": "20"},          # 매출총이익률
    {"field": "operatingmargin", "operator": "gt", "value": "15"},      # 영업이익률
    {"field": "roe", "operator": "gt", "value": "10"},                  # 자기자본이익률
    {"field": "roic", "operator": "gt", "value": "8"},                  # 투자자본수익률

    # 재무안정성 지표 (4개)
    {"field": "currentratio", "operator": "gt", "value": "1.5"},        # 유동비율
    {"field": "debttoequity", "operator": "lt", "value": "1"},          # 부채비율
    {"field": "netdebttoebitda", "operator": "lt", "value": "3"},       # 순부채/EBITDA
    {"field": "altmanzscore", "operator": "gt", "value": "3"},          # 알트만 Z-스코어

    # 밸류에이션 지표 (4개)
    {"field": "pricetoearnings", "operator": "lt", "value": "20"},      # P/E
    {"field": "pricetobook", "operator": "lt", "value": "3"},           # P/B
    {"field": "evtoebitda", "operator": "lt", "value": "12"},           # EV/EBITDA
    {"field": "dividendyield", "operator": "gt", "value": "2"},         # 배당수익률

    # 현금흐름 지표 (3개)
    {"field": "freecashflow", "operator": "gt", "value": "0"},          # 잉여현금흐름
    {"field": "ocftocapex", "operator": "gt", "value": "1.2"},         # OCF/CAPEX
    {"field": "ocfqoqgrowth", "operator": "gt", "value": "0"},         # 분기 영업현금흐름 성장률

    # 기업규모 지표 (1개)
    {"field": "marketcap", "operator": "gt", "value": "1000000000"}     # 시가총액 10억 달러 이상
]

# 논리 연산자 설정
logic = SecurityScreenGroup(operator="AND", clauses=clauses)

# 정렬 설정
order_column = 'marketcap'
order_direction = 'desc'
primary_only = True
page_size = 100

try:
    response = SecurityApi().screen_securities(
        logic=logic,
        order_column=order_column,
        order_direction=order_direction,
        primary_only=primary_only,
        page_size=page_size
    )
    print(response)
    
except ApiException as e:
    print("Exception when calling SecurityApi->screen_securities: %s\n" % e)