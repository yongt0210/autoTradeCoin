from fastapi import APIRouter

from app.router import backtest

api_router = APIRouter()

api_router.include_router(backtest.router, prefix="/backtest")