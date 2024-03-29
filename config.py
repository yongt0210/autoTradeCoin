from starlette.config import Config
import os

# path = os.path.dirname(os.path.realpath(__file__))

config = Config('.env')

# 빗썸 API 키값
CONNECT_KEY: str = config("connect_key")
SECRET_KEY: str = config("secret_key")

# 코인 심볼(BTC: 비트코인, ETH: 이더리움, XRP: 리플, SOL: 솔라나)
coin_list: list = ["BTC", "ETH", "XRP", "SOL"]

# 빗썸 수수료(0.04%)
rate : float = 0.0004

realserver: bool = config("realserver") == "True"