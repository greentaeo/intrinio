from fastapi import APIRouter, HTTPException, Request  # Request 추가
from typing import Dict, Optional, Any
from pydantic import BaseModel, ValidationError  # ValidationError 추가
from app.services.screener.screener_service import FlexibleScreener
from app.services.screener.constants import AVAILABLE_METRICS, OPERATORS

router = APIRouter()
screener = FlexibleScreener()

CATEGORY_MAPPING = {
    "위험성 지표": "Risk",     # 이 매핑이 있는지 확인
    "산업 분류": "Industry",
    "시가총액 지표": "MarketCap",
    "성장성 지표": "Growth",
    "수익성 지표": "Profitability",
    "재무안정성 지표": "Stability",
    "밸류에이션 지표": "Valuation",
    "현금흐름 지표": "CashFlow"
}
# GET 엔드포인트 추가
@router.get("")
async def get_screener_data():
    try:
        # 기본 조건으로 데이터 조회
        results = screener.screen_by_criteria(
            criteria={"operator": "AND", "clauses": []},
            page=1,
            limit=100
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"데이터 조회 중 오류가 발생했습니다: {str(e)}"
        )
    
class FilterValue(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
    value: Optional[str] = None
    operator: Optional[str] = None

@router.post("/filter")
async def filter_stocks(request: Request):
    try:
        body = await request.json()
        print("Raw request body:", body)
        
        conditions = []
        for kr_category, metrics in body.items():
            category = CATEGORY_MAPPING.get(kr_category)
            if not category:
                continue
                
            category_metrics = AVAILABLE_METRICS.get(category, {})
            
            for metric_id, values in metrics.items():
                if metric_id in category_metrics:
                    if isinstance(values, dict):  # 딕셔너리 형태로 들어오는 경우
                        if 'value' in values:  # 단일 값
                            conditions.append({
                                "field": metric_id,
                                "operator": "eq",
                                "value": str(values['value'])
                            })
                        else:  # min/max 범위
                            if values.get('min') is not None:
                                conditions.append({
                                    "field": metric_id,
                                    "operator": "gt",
                                    "value": str(values['min'])
                                })
                            if values.get('max') is not None:
                                conditions.append({
                                    "field": metric_id,
                                    "operator": "lt",
                                    "value": str(values['max'])
                                })

        if not conditions:
            raise HTTPException(
                status_code=400,
                detail="유효한 필터 조건이 없습니다."
            )
        
        criteria = {
            "operator": "AND",
            "clauses": conditions
        }
        
        print("Final API request:", criteria)
        results = screener.screen_by_criteria(criteria=criteria)
        return results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"필터링 중 오류가 발생했습니다: {str(e)}"
        )