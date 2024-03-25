import requests

from app.bithumb.bithumb import Bithumb

class Bithumb_Private(Bithumb):
    def __init__(self):
        super().__init__()

    # 내 정보 및 코인 수수료 확인
    def get_my_info(self, order_currency="BTC", payment_currency="KRW"):
        data = {
            'order_currency': order_currency, 
            "payment_currency": payment_currency
        }

        uri = "/info/account"

        headers = self.set_secret_header(uri=uri, data=data)

        url = '{api_url}{uri}'.format(api_url=self.api_url, uri=uri)

        res = requests.post(url, headers=headers, data=data)

        result = res.json()

        if result['status'] == "0000":
            return result['data']
        else:
            None

    # 현재 내 자산 구하기
    def get_my_account(self, currency="ALL"):
        data = {
            'currency': currency
        }

        uri = "/info/balance"

        headers = self.set_secret_header(uri=uri, data=data)

        url = '{api_url}{uri}'.format(api_url=self.api_url, uri=uri)

        res = requests.post(url, headers=headers, data=data)

        result = res.json()

        if result['status'] == "0000":
            return result['data']
        else:
            None

    # 시장가에 사기
    def buy_market_price(
        self
        , units
        , order_currency="BTC"
        , payment_currency="KRW"
    ):
        '''
        시장가에 팔기
        units: 개수
        order_currency: 코인 티커
        payment_currency: BTC or KRW
        '''
        data = {
            'units': units,
            "order_currency": order_currency,
            "payment_currency": payment_currency,
        }

        uri = "/trade/market_buy"

        headers = self.set_secret_header(uri=uri, data=data)

        url = '{api_url}{uri}'.format(api_url=self.api_url, uri=uri)

        res = requests.post(url, headers=headers, data=data)

        result = res.json()

        if result['status'] == "0000":
            return result['order_id']
        else:
            None

    # 시장가에 팔기
    def sell_market_price(
        self
        , units
        , order_currency="BTC"
        , payment_currency="KRW"
    ):
        '''
        시장가에 팔기
        units: 개수
        order_currency: 코인 티커
        payment_currency: BTC or KRW
        '''
        data = {
            'units': units,
            "order_currency": order_currency,
            "payment_currency": payment_currency,
        }

        uri = "/trade/market_sell"

        headers = self.set_secret_header(uri=uri, data=data)

        url = '{api_url}{uri}'.format(api_url=self.api_url, uri=uri)

        res = requests.post(url, headers=headers, data=data)

        result = res.json()

        if result['status'] == "0000":
            return result['order_id']
        else:
            None

    
bithumb_private = Bithumb_Private()