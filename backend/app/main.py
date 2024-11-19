from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 이 부분만 수정
from .api.screener.routes import router as screener_router  # 상대 경로로 변경

# 나머지 코드는 그대로...
# 나머지 코드는 동일하게 유지...
app = FastAPI(title="Screener API")

# CORS 설정을 더 구체적으로
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite 기본 포트
    "http://127.0.0.1:5173",
]

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 스크리너 라우터 등록
app.include_router(
    screener_router,
    prefix="/api/screener",
    tags=["screener"]
)

# 헬스체크 엔드포인트 추가
@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "message": "Screener API is running"}