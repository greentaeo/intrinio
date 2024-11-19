from typing import Dict, List
from fastapi import HTTPException
import requests
from datetime import datetime
from .constants import AVAILABLE_METRICS, format_value
import math

class FlexibleScreener:
    def __init__(self):
        self.api_key = "OjI1NDJiNjBlOWY5YTI1NTMzOTZjYzNiODBjNmFmNGNk"
        self.base_url = "https://api-v2.intrinio.com/securities/screen"
        self.last_criteria = {}

    def screen_by_criteria(
        self, 
        criteria: Dict, 
        page: int = 1, 
        limit: int = 100,
        sort_by: str = None,
        order: str = "desc"
    ) -> Dict:
        try:
            print("Screener received criteria:", criteria)
            
            # API 호출 및 raw 데이터 획득
            raw_results = self._fetch_from_api(criteria)
            print("Raw API response:", raw_results)  # 디버깅
            
            # 데이터 가공
            processed_results = self._process_results(raw_results)
            print("Processed results:", processed_results)  # 디버깅
            
            # 정렬 적용
            if sort_by:
                processed_results = self._sort_results(processed_results, sort_by, order)
            
            # 페이지네이션 적용
            total_results = len(processed_results)
            total_pages = math.ceil(total_results / limit)
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            paged_results = processed_results[start_idx:end_idx]
            
            # 숫자 포맷팅 적용
            formatted_results = []
            for item in paged_results:
                formatted_item = item.copy()
                for metric, value in item.items():
                    if metric not in ['id', 'ticker', 'name', 'exchange'] and value is not None:
                        formatted_item[metric] = format_value(metric.lower(), value)
                formatted_results.append(formatted_item)
            
            return {
                'status': 'success',
                'pagination': {
                    'current_page': page,
                    'total_pages': total_pages,
                    'total_items': total_results,
                    'items_per_page': limit
                },
                'sort': {
                    'field': sort_by,
                    'order': order
                } if sort_by else None,
                'data': formatted_results,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'filters_applied': criteria
                }
            }
            
        except Exception as e:
            print(f"Error in screen_by_criteria: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def _fetch_from_api(self, criteria: Dict) -> List[Dict]:
        """인트리니오 API 호출"""
        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            print("Making API request with criteria:", criteria)
            response = requests.post(self.base_url, headers=headers, json=criteria)
            
            if response.status_code != 200:
                print(f"API Error Response: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Intrinio API error: {response.text}"
                )
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"API 호출 중 오류 발생: {str(e)}"
            )

    def _process_results(self, raw_results: List[Dict]) -> List[Dict]:
        """API 응답을 프론트엔드 친화적인 형태로 가공"""
        processed_results = []
        
        for item in raw_results:
            security = item.get('security', {})
            data_points = {
                d['tag']: d.get('number_value')
                for d in item.get('data', [])
            }
            
            processed_item = {
                'id': security.get('id'),
                'ticker': security.get('ticker'),
                'name': security.get('name'),
                'exchange': security.get('exchange') or 'US',
                **data_points  # 모든 데이터 포인트 추가
            }
            
            processed_results.append(processed_item)
        
        return processed_results

    def _sort_results(self, results: List[Dict], sort_by: str, order: str = "desc") -> List[Dict]:
        """결과 정렬"""
        def get_sort_key(item):
            value = item.get(sort_by)
            if value is None:
                return float('-inf') if order.lower() == "desc" else float('inf')
            try:
                return float(value)
            except (TypeError, ValueError):
                return float('-inf') if order.lower() == "desc" else float('inf')
        
        return sorted(
            results,
            key=get_sort_key,
            reverse=(order.lower() == "desc")
        )