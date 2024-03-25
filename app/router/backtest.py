import math
import pandas as pd
from pandas import DataFrame
from typing import Any
from fastapi import APIRouter

from app.bithumb.public import bithumb_public
from app.lib.function import generate_signals
from config import rate

router = APIRouter()

@router.get("/{code}")
async def get_common_code_root(
    *,
    code: str,
) -> list:
    data = bithumb_public.get_ohlcv_chart_data(code)

    # 5일 이동평균선 
    signal = generate_signals(data, window=5, k=0.5)

    # 초기 투자금액 백만원으로 설정
    money = 1000000

    result = []

    for i in signal.index:
        # 구입가
        buy_money = math.floor(signal["target"][i] * (1 / (1 - rate)))

        # 판매가
        sell_money = math.floor(signal["close"][i] * (1 - rate))

        money = math.floor(money * sell_money / buy_money)
        
        result.append({
            "date" : i,
            "rate": round(((sell_money / buy_money) - 1) * 100, 2),
            "money": money, 
            "buy_money": signal["target"][i],
            "buy_money_fee": buy_money,
            "sell_money": signal["close"][i],
            "sell_money_fee": sell_money,
        })

    return result