import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.bithumb.public import bithumb_public
from app.scheduler.trade import scheduler
from app.router import api_router

app = FastAPI(
    title="가상화폐 자동 투자",
    description="빗썸 API를 이용한 가상화폐 자동 투자",
    version="0.0.1",
    openapi_url="/api/openapi.json",
    debug=True
)

# 미들웨어 세팅
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router)

@app.on_event("startup")
async def startup():
    print("start service")

    # 스케줄러 실행
    scheduler.start()  

@app.get("/")
def startProcess():
    data = bithumb_public.get_ohlcv_chart_data("SOL")
    return data

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)