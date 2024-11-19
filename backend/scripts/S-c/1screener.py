# screener_flexible.py

from intrinio_sdk import SecurityApi, ApiClient
from intrinio_sdk.rest import ApiException
import logging
import json
from datetime import datetime
import time
import pandas as pd

class FlexibleScreener:
    def __init__(self):
        self.api_client = ApiClient()
        self.api_client.set_api_key('OjI1NDJiNjBlOWY5YTI1NTMzOTZjYzNiODBjNmFmNGNk')
        self.api_client.allow_retries(True)
        self.security_api = SecurityApi()
        
        # 로깅 설정
        self.logger = self._setup_logger()
        
        # 스크리너 설정 로드
        self.config = ScreenerConfig()
        
    def _setup_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return logging.getLogger(__name__)

    def screen_by_categories(self, selected_categories=None, selected_groups=None):
        """선택된 카테고리와 그룹으로 스크리닝"""
        try:
            # 모든 필터 조건을 저장할 리스트
            all_clauses = []
            
            for category_name, category_data in self.config.filter_categories.items():
                if selected_categories and category_name not in selected_categories:
                    continue
                    
                for group_name, group_data in category_data["groups"].items():
                    if selected_groups and group_name not in selected_groups:
                        continue
                        
                    for metric, metric_data in group_data["metrics"].items():
                        clause = {
                            "field": metric,
                            "operator": metric_data["operator"],
                            "value": metric_data["value"]
                        }
                        all_clauses.append(clause)
            
            if not all_clauses:
                self.logger.warning("선택된 필터가 없습니다.")
                return []
            
            # 필터 조건 구성
            screen_filter = {
                "operator": "OR",
                "clauses": all_clauses
            }
            
            self.logger.info(f"스크리닝 시작: {len(all_clauses)}개 조건")
            
            # API 호출
            api_instance = SecurityApi()
            result = api_instance.screen_securities(logic=screen_filter)
            
            # API 응답 처리 수정
            if result and isinstance(result, list):
                tickers = []
                for item in result:
                    if hasattr(item, 'security') and item.security:
                        security = item.security
                        if hasattr(security, 'ticker'):
                            tickers.append(security.ticker)
                        elif hasattr(security, 'symbol'):
                            tickers.append(security.symbol)
                
                if tickers:
                    self.logger.info(f"검색된 기업 수: {len(tickers)}")
                    return tickers
            
            self.logger.warning("스크리닝 결과가 없습니다.")
            return []
            
        except ApiException as e:
            self.logger.error(f"스크리닝 중 API 에러 발생: {str(e)}")
            return []
        
        except Exception as e:
            self.logger.error(f"예상치 못한 에러 발생: {str(e)}")
            self.logger.error(f"에러 타입: {type(e)}")
            import traceback
            self.logger.error(f"상세 에러: {traceback.format_exc()}")
            return []

    def get_company_details(self, tickers, selected_categories=None):
        """선택된 카테고리의 지표들에 대한 기업 상세 정보 조회"""
        details = []
        
        for ticker in tickers:
            try:
                company = self.security_api.get_security_by_id(ticker)
                metrics = {}
                
                # 선택된 카테고리의 지표들만 조회
                for category_name, category_data in self.config.filter_categories.items():
                    if selected_categories and category_name not in selected_categories:
                        continue
                        
                    for group_data in category_data["groups"].values():
                        for metric in group_data["metrics"].keys():
                            value = getattr(company, metric, None)
                            if value is not None:
                                metrics[metric] = value
                
                company_detail = {
                    "ticker": ticker,
                    "name": getattr(company, 'name', ''),
                    "exchange": getattr(company, 'exchange_ticker', ''),
                    "metrics": metrics
                }
                
                details.append(company_detail)
                self.logger.info(f"기업 정보 조회 완료: {ticker}")
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"기업 정보 조회 실패 - {ticker}: {str(e)}")
                
        return details

    def save_results(self, results, selected_categories, selected_groups):
        """스크리닝 결과 저장"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screening_results_{timestamp}.json"
            
            data = {
                "timestamp": timestamp,
                "selected_categories": selected_categories,
                "selected_groups": selected_groups,
                "results": results
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            return filename
            
        except Exception as e:
            self.logger.error(f"결 저장 중 에러 발생: {str(e)}")
            return None
        
    def print_company_details(self, company_data):
        """기업 상세 정보 출력"""
        self.logger.info("\n=== 기업 상세 정보 ===")
        self.logger.info(f"티커: {company_data.get('ticker')}")
        self.logger.info(f"기업명: {company_data.get('name')}")
        self.logger.info(f"\n[성장성]")
        self.logger.info(f"• 순이익 성장률: {company_data.get('netincomegrowth')}%")
        self.logger.info(f"• 매출 성장률: {company_data.get('revenuegrowth')}%")
        self.logger.info(f"\n[수익성]")
        self.logger.info(f"• 영업이익률: {company_data.get('operatingmargin')}%")
        self.logger.info(f"• 순이익률: {company_data.get('profitmargin')}%")
        self.logger.info(f"\n[가치평가]")
        self.logger.info(f"• PER: {company_data.get('pricetoearnings')}배")
        self.logger.info(f"• PBR: {company_data.get('pricetobook')}배")
        self.logger.info(f"• EV/EBITDA: {company_data.get('evtoebitda')}배")

    def save_to_csv(self, company_details, filename):
        """결과를 CSV 파일로 저장"""
        df = pd.DataFrame(company_details)
        df.to_csv(filename, index=False)
        self.logger.info(f"CSV 파일로 저장되었습니다: {filename}")

class ScreenerConfig:
    """스크리너 설정 클래스"""
    def __init__(self):
        self.filter_categories = {
            "growth_metrics": {
                "name": "성장성 지표",
                "groups": {
                    "earnings_growth": {
                        "name": "이익 성장률",
                        "metrics": {
                            "netincomegrowth": {"name": "순이익 성장률", "operator": "gt", "value": "-5"},
                            "epsgrowth": {"name": "EPS 성장률", "operator": "gt", "value": "-5"}
                        }
                    },
                    "operation_growth": {
                        "name": "영업 성장률",
                        "metrics": {
                            "revenuegrowth": {"name": "매출 성장률", "operator": "gt", "value": "0"}
                        }
                    }
                }
            },
            "profitability_metrics": {
                "name": "수익성 지표",
                "groups": {
                    "margin_ratios": {
                        "name": "이익률",
                        "metrics": {
                            "operatingmargin": {"name": "영업이익률", "operator": "gt", "value": "3"},
                            "profitmargin": {"name": "순이익률", "operator": "gt", "value": "1"}
                        }
                    }
                }
            },
            "valuation_metrics": {
                "name": "가치평가 지표",
                "groups": {
                    "price_ratios": {
                        "name": "주가 배수",
                        "metrics": {
                            "pricetoearnings": {"name": "PER", "operator": "lt", "value": "25"},
                            "pricetobook": {"name": "PBR", "operator": "lt", "value": "3"},
                            "evtoebitda": {"name": "EV/EBITDA", "operator": "lt", "value": "15"}
                        }
                    }
                }
            }
        }
       

def main():
    screener = FlexibleScreener()
    
    # 각 카테고리별 스크리닝 결과를 저장할 딕셔너리
    category_results = {}
    
    # 모든 카테고리 테스트
    categories_to_test = [
        "growth_metrics",
        "profitability_metrics",
        "valuation_metrics"
    ]
    
    for category in categories_to_test:
        screener.logger.info("\n" + "="*50)
        screener.logger.info(f"테스트 카테고리: {category}")
        screener.logger.info("="*50)
        
        # 해당 카테고리의 모든 그룹 선택
        selected_groups = []
        category_data = screener.config.filter_categories.get(category, {})
        selected_groups.extend(list(category_data.get("groups", {}).keys()))
        
        # 스크리닝 실행
        passing_companies = screener.screen_by_categories(
            selected_categories=[category],
            selected_groups=selected_groups
        )
        
        if passing_companies:
            category_results[category] = set(passing_companies)
    
    # 모든 조건을 만족하는 기업 찾기
    if category_results:
        common_companies = set.intersection(*category_results.values())
        
        screener.logger.info("\n" + "="*50)
        screener.logger.info(f"모든 조건을 만족하는 기업: {len(common_companies)}개")
        screener.logger.info("="*50)
        
        if common_companies:
            # 최종 기업들의 상세 정보 조회
            company_details = screener.get_company_details(
                list(common_companies),
                selected_categories=categories_to_test
            )
            
            # 결과 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"final_screening_results_{timestamp}.json"
            saved_file = screener.save_results(
                company_details,
                categories_to_test,
                []
            )
            
            if saved_file:
                screener.logger.info(f"최종 스크리닝 결과가 저장되었습니다: {saved_file}")
        else:
            screener.logger.info("\n모든 조건을 만족하는 기업이 없습니다.")

if __name__ == "__main__":
    main()