from fastapi import APIRouter, HTTPException, Request  # Request 추가
from typing import Dict, Optional, Any
from pydantic import BaseModel, ValidationError  # ValidationError 추가
from app.services.screener.screener_service import FlexibleScreener
from app.services.screener.constants import AVAILABLE_METRICS, OPERATORS
import json
from pathlib import Path

# SIC_HIERARCHY 데이터 로드
sic_file_path = Path(__file__).parent.parent.parent / "services" / "screener" / "data" / "sic_hierarchy.json"
with open(sic_file_path, "r", encoding="utf-8") as f:
    SIC_HIERARCHY = json.load(f)

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

def format_sic_code(code: str) -> str:
    """SIC 코드를 형식에 맞게 변환"""
    try:
        # 숫자만 추출
        numeric_code = ''.join(filter(str.isdigit, code))
        if len(numeric_code) == 4:
            return numeric_code  # 콤마 없이 순수 숫자로만
    except Exception as e:
        print(f"Error formatting SIC code: {e}")
    return code

@router.post("/filter")
async def filter_stocks(request: Request):
    try:
        body = await request.json()
        print("Raw request body:", body)
        
        conditions = []
        for kr_category, metrics in body.items():
            category = CATEGORY_MAPPING.get(kr_category)
            print(f"Processing category: {kr_category} -> {category}")
            
            if not category:
                continue
                
            if category == "Industry":
                for metric_id, values in metrics.items():
                    print(f"Processing metric: {metric_id} with values: {values}")
                    
                    if isinstance(values, dict):
                        if metric_id == "sic":
                            if 'value' in values:
                                formatted_code = format_sic_code(values['value'])
                                conditions.append({
                                    "field": "sic",
                                    "operator": values.get('operator', 'eq'),
                                    "value": formatted_code
                                })
                            elif 'min' in values or 'max' in values:
                                # min과 max를 개별 조건으로 추가
                                if values.get('min'):
                                    conditions.append({
                                        "field": "sic",
                                        "operator": "gte",
                                        "value": format_sic_code(values['min'])
                                    })
                                if values.get('max'):
                                    conditions.append({
                                        "field": "sic",
                                        "operator": "lte",
                                        "value": format_sic_code(values['max'])
                                    })

        if not conditions:
            raise HTTPException(
                status_code=400,
                detail="유효한 필터 조건이 없습니다."
            )
        
        # 최상위 레벨에서 AND 조건으로 묶기
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

@router.get("/industry-hierarchy")
async def get_industry_hierarchy(
    division_code: Optional[str] = None,
    major_group_code: Optional[str] = None
):
    """산업 계층 구조 조회 API"""
    try:
        if not division_code:
            # 대분류 목록 반환
            return {
                code: {
                    "name": data["name"],
                    "name_en": data["name_en"]
                }
                for code, data in SIC_HIERARCHY["sic_codes"].items()
            }
        
        division = SIC_HIERARCHY["sic_codes"].get(division_code)
        if not division:
            raise HTTPException(status_code=404, detail="산업 대분류를 찾을 수 없습니다")
            
        if not major_group_code:
            # 중분류 목록 반환
            return {
                code: {
                    "name": data["name"],
                    "name_en": data["name_en"]
                }
                for code, data in division["subcategories"].items()
            }
            
        major_group = division["subcategories"].get(major_group_code)
        if not major_group:
            raise HTTPException(status_code=404, detail="산업 중분류를 찾을 수 없습니다")
            
        # 세부 산업 목록 반환
        return {
            code: {
                "name": data["name"]
            }
            for code, data in major_group["subcategories"].items()
        }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))