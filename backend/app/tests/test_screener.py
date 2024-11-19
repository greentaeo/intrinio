from app.services.screener.screener_service import FlexibleScreener
import asyncio

async def main():
    # 테스트용 criteria 예시
    test_criteria = {
        "marketcap": ("gt", 1000000000),  # 시가총액 10억 달러 이상
        "pricetoearnings": ("gt", 10)  # P/E 비율 10 이상
    }

    try:
        screener = FlexibleScreener()
        results = await screener.screen_by_criteria(test_criteria)
        print("스크리닝 결과:", results)
    except Exception as e:
        print("에러 발생:", str(e))

if __name__ == "__main__":
    # asyncio.run()을 사용하여 비동기 함수 실행
    asyncio.run(main()) 