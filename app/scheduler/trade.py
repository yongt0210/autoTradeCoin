import math
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler

from config import coin_list

from app.bithumb.private import bithumb_private
from app.bithumb.public import bithumb_public
from app.lib.function import makeDataFrame, generate_signals, get_now_time

scheduler = BackgroundScheduler(timezone='Asia/Seoul')

@scheduler.scheduled_job('cron', second='*/5', id='autotrade')
def auto_trading():
    """
    5초마다 돌파 신호가 오면 매수
    정오에 보유 코인 전부 매도
    """
    today_time = get_now_time("%H:%M:%S")

    my_account = bithumb_private.get_my_account()

    # 정오때 전부 매매
    if today_time == "00:00:00":
        sell_all_coins(my_account)
    
    str = "[{time}] scheduler test".format(time=get_now_time("%H:%M:%S"))
    print(str)


# 모든 코인 다 팔기
async def sell_all_coins(my_account):
    for coin in coin_list:
        key = "available_{coin}".format(coin=coin.lower())

        units = float(my_account[key])

        # 현재 0.001 넘게 가지고 있는 코인만 팔기(최소 거래량이 0.0001)
        if not units >= 0.0001:
            continue
        
        await bithumb_private.sell_market_price(
            units=units
            , order_currency=coin
        )

# 추세를 보면서 코인 사기 
async def check_and_buy_coins(my_account):
    """
    추세를 보면서 
    """

    # 코인당 투자금액
    available_money = get_available_money(my_account["total_krw"], len(coin_list))

    for coin in coin_list:
        key = "available_{coin}".format(coin=coin.lower())

        units = float(my_account[key])

        # 이미 구매했으면(이미 코인을 가지고 있으면) 다음 코인 확인
        if units >= 0.0001:
            continue

        await get_coin_signals_units(coin, available_money)


async def get_coin_signals_units(coin, money) -> Any:
    today = get_now_time('%Y-%m-%d')

    data = bithumb_public.get_ohlcv_chart_data(coin, interval="24h")
    df = makeDataFrame(data=data)

    signals = generate_signals(df=df, k=0.5, window=5)

    # 오늘 매수 시점이 안보이면 종료
    if today != max(signals.index):
        return None

    # 현재가가 목표가를 넘지 못하면 종료
    if signals.iloc[-1]["close"] < signals.iloc[-1]["target"]:
        return None
    
    # 코인 개수(0.0001 이상부터 거래 가능하므로 소수점 4자리 이하는 버림)
    units = unit_floor(money / signals.iloc[-1]["close"])

    # 거래 최소 조건인 0.0001 이하면 종료
    if not units >= 0.0001:
        return None
    
    buy_result = await bithumb_private.buy_market_price(
        units=units
        , order_currency=coin
    )

    return buy_result

# 투자 가용 금액 구하기
def get_available_money(total_money, coin_len):
    """
    투자 가용 금액 구하기
    * 코인당 최대 투자 가용 금액: 전체 보유금액의 20% 중에서 투자 코인수만큼 나누기
    """

    # 현재 가지고 있는 돈 
    total_money = math.floor(float(total_money))

    # 현재 가지고 있는 돈의 20%만 투자
    available_money = math.floor(total_money * 0.2 * (1/coin_len))

    return available_money

# 소수점 4자리에서 버림
def unit_floor(unit):
    return math.floor(unit * 10000) / 10000