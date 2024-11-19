AVAILABLE_METRICS = {
    "MarketCap": {  # 새로 추가
        "marketcap": "시가총액",
        "enterprisevalue": "기업가치"
    },
    "Growth": {
        "revenuegrowth": "매출액 성장률",
        "netincomegrowth": "순이익 성장률",
        "epsgrowth": "주당순이익 성장률",
        "ebitdagrowth": "EBITDA 성장률",
        "ebitgrowth": "EBIT 성장률",
        "ocfgrowth": "영업현금흐름 성장률",
        "fcffgrowth": "잉여현금흐름 성장률"
    },
    "Profitability": {
        "grossmargin": "매출총이익률",
        "operatingmargin": "영업이익률",
        "profitmargin": "순이익률",
        "ebitdamargin": "EBITDA 마진",
        "roe": "자기자본이익률",
        "roa": "총자산이익률",
        "roic": "투하자본수익률"
    },
    "Stability": {
        "currentratio": "유동비율",
        "quickratio": "당좌비율",
        "nwc": "순운전자본",
        "debttoequity": "부채비율",
        "debttoebitda": "부채/EBITDA",
        "netdebttoebitda": "순부채/EBITDA",
        "ltdebttoequity": "장기부채/자기자본",
        "ebittointerestex": "EBIT/이자비용",
        "altmanzscore": "알트만 Z-Score",
        "debttototalcapital": "부채/총자본"
    },
    "Valuation": {  # marketcap, enterprisevalue 제거
        "pricetoearnings": "P/E 비율",
        "pricetobook": "P/B 비율",
        "evtoebitda": "EV/EBITDA",
        "pricetorevenue": "P/S 비율",
        "dividendyield": "배당수익률",
        "earningsyield": "이익수익률"
    },
    "CashFlow": {
        "freecashflow": "잉여현금흐름",
        "ocfgrowth": "영업현금흐름 성장률",
        "capex": "설비투자",
        "ocftocapex": "OCF/CAPEX"
    }
}

# 연산자 정의
OPERATORS = {
    "gt": "초과",
    "lt": "미만",
    "gte": "이상",
    "lte": "이하",
    "eq": "같음",
    "between": "범위"
}

# 값 포맷팅 함수
def format_value(metric: str, value: float) -> str:
    """지표별 값 포맷팅"""
    if value is None:
        return 'N/A'
    
    # 비율 지표들 (%)
    percent_metrics = [
        'revenuegrowth', 'netincomegrowth', 'epsgrowth', 'ebitdagrowth',
        'ebitgrowth', 'ocfgrowth', 'fcffgrowth', 'grossmargin', 
        'operatingmargin', 'profitmargin', 'ebitdamargin', 'roe', 'roa',
        'roic', 'currentratio', 'quickratio', 'debttoequity', 'ltdebttoequity',
        'debttototalcapital', 'dividendyield', 'earningsyield'
    ]
    
    # 배수 지표들 (x)
    multiple_metrics = [
        'debttoebitda', 'netdebttoebitda', 'ebittointerestex',
        'pricetoearnings', 'pricetobook', 'evtoebitda', 'pricetorevenue',
        'ocftocapex'  # OCF/CAPEX 추가
    ]
    
    try:
        if metric in percent_metrics:
            return f"{value:,.1f}%"
        elif metric in multiple_metrics:
            return f"{value:,.1f}x"
        elif metric in ['marketcap', 'enterprisevalue', 'freecashflow', 'capex']:
            if value >= 1_000_000_000:
                return f"{value/1_000_000_000:,.1f}B"
            else:
                return f"{value/1_000_000:,.1f}M"
        elif metric == 'altmanzscore':
            return f"{value:,.2f}"
        else:
            return f"{value:,g}"
    except (TypeError, ValueError):
        return 'N/A'