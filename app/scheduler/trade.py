from apscheduler.schedulers.background import BackgroundScheduler

from config import coin_list
from app.lib.function import get_now_time
from app.bithumb.private import bithumb_private

scheduler = BackgroundScheduler(timezone='Asia/Seoul')

@scheduler.scheduled_job('cron', second='*/5', id='autotrade')
def auto_trading():
    """
    스케줄러 임시 테스트
    """
    now = get_now_time("%H:%M:%S")

    my_account = bithumb_private.get_my_account()

    # 정오때 전부 매매
    if now == "00:00:00":
        for coin in coin_list:
            units = float(my_account["available_"+coin.lower()])

            # 현재 0.001 넘게 가지고 있는 코인만 팔기(최소 거래량이 0.0001)
            if not units >= 0.0001:
                continue
            
            bithumb_private.sell_market_price(
                units=units
                , order_currency=coin
            )

    
    str = "[{time}] scheduler test".format(time=get_now_time("%H:%M:%S"))
    print(str)
