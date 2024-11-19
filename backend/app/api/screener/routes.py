from fastapi import APIRouter, HTTPException, Request  # Request 추가
from typing import Dict, Optional, Any
from pydantic import BaseModel, ValidationError  # ValidationError 추가
from app.services.screener.screener_service import FlexibleScreener
from app.services.screener.constants import AVAILABLE_METRICS, OPERATORS

router = APIRouter()
screener = FlexibleScreener()

CATEGORY_MAPPING = {
    "시가총액 지표": "MarketCap",     # 추가
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

@router.post("/filter")
async def filter_stocks(request: Request, filters: Dict[str, Dict[str, FilterValue]]):
    try:
        # 원본 요청 데이터 로깅
        body = await request.json()
        print("Raw request body:", body)
        print("Parsed filters:", filters)
        
        # 필터 유효성 검사
        if not isinstance(filters, dict):
            raise HTTPException(
                status_code=422,
                detail="필터는 딕셔너리 형태여야 합니다."
            )
        
        # Intrinio API 조건 형식으로 직접 변환
        conditions = []
        for kr_category, metrics in filters.items():
            print(f"Processing category: {kr_category}")
            category = CATEGORY_MAPPING.get(kr_category)
            if not category:
                print(f"Warning: Unknown category {kr_category}")
                continue
                
            category_metrics = AVAILABLE_METRICS.get(category, {})
            print(f"Category metrics for {category}:", category_metrics)
            
            if not isinstance(metrics, dict):
                print(f"Warning: Invalid metrics format for {kr_category}")
                continue
                
            for metric_id, values in metrics.items():
                print(f"Processing metric: {metric_id} with values: {values}")
                if metric_id in category_metrics:
                    try:
                        if values.min is not None:
                            conditions.append({
                                "field": metric_id,
                                "operator": "gt",
                                "value": float(values.min)
                            })
                        if values.max is not None:
                            conditions.append({
                                "field": metric_id,
                                "operator": "lt",
                                "value": float(values.max)
                            })
                    except (ValueError, AttributeError) as e:
                        print(f"Error processing values for {metric_id}: {e}")
                else:
                    print(f"Warning: Unknown metric {metric_id} for category {category}")

        print("Generated API conditions:", conditions)
        
        if not conditions:
            raise HTTPException(
                status_code=400,
                detail="유효한 필터 조건이 없습니다."
            )
        
        # Intrinio API 요청 형식
        criteria = {
            "operator": "AND",
            "clauses": conditions
        }
        
        print("Final API request:", criteria)
        
        results = screener.screen_by_criteria(
            criteria=criteria,
            page=1,
            limit=100
        )
        
        return results
        
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise HTTPException(
            status_code=422,
            detail=f"데이터 형식이 올바르지 않습니다: {str(e)}"
        )
    except Exception as e:
        print(f"Error in filter_stocks: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"필터링 중 오류가 발생했습니다: {str(e)}"
        )