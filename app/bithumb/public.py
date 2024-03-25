import requests
from datetime import datetime

from app.bithumb.bithumb import Bithumb
# from app.lib.function import timestamp_to_datetime

class Bithumb_Public(Bithumb):
    def __init__(self):
        super().__init__()

    # 현재가 정보 조회(자산별: 코인 스택, 전체: ALL)
    def get_current_price(self, ticker="BTC", money="KRW"):
        url = '{api_url}/public/ticker/{ticker}_{money}'.format(api_url=self.api_url, ticker=ticker, money=money)

        res = requests.get(url)

        return res.json()

    # 차트 데이터 조회
    def get_ohlcv_chart_data(self, ticker="BTC", money="KRW", interval="24h"):
        url = '{api_url}/public/candlestick/{ticker}_{money}/{interval}'.format(api_url=self.api_url, ticker=ticker, money=money, interval=interval)

        res = requests.get(url)

        result = res.json()

        data = []

        # 데이터 호출 성공
        if result['status'] == '0000':
            data = result["data"]
            # for item in result['data']:
            #     data.append({
            #         'datetime': timestamp_to_datetime(item[0], interval),
            #         'open': float(item[1]),
            #         'close': float(item[2]),
            #         'high': float(item[3]),
            #         'low': float(item[4]),
            #         'volume': float(item[5]),
            #     })
        

        return data

bithumb_public = Bithumb_Public()