import math
import time
import hmac, hashlib, urllib.parse, base64

from config import CONNECT_KEY, SECRET_KEY

class Bithumb:
    api_url = 'https://api.bithumb.com'

    def __init__(self):
        self.connect_key = CONNECT_KEY
        self.secret_key = SECRET_KEY

    # 소수점 4자리 반올림
    def unit_floor(self, unit):
        return math.floor(unit * 10000) / 10000
    
    # nonce 값 구하기
    def get_nonce_time(self):
        nonce = str(int(time.time() * 1000))

        return nonce
    
    def microtime(self, get_as_float = False):
        if get_as_float:
            return time.time()
        else:
            return '%f %d' % math.modf(time.time())

    def usecTime(self) :
        mt = self.microtime(False)
        mt_array = mt.split(" ")[:2]
        return mt_array[1] + mt_array[0][2:5]
    
    # 인증키 값(헤더) 만들기
    def set_secret_header(self, uri, data):
        data["endpoint"] = uri

        key = self.secret_key.encode('utf-8')

        str_data = urllib.parse.urlencode(data)

        nonce = self.usecTime()

        query_string = uri + chr(0) + str_data + chr(0) + nonce
        h = hmac.new(bytes(key), query_string.encode('utf-8'), hashlib.sha512)
        hex_output = h.hexdigest().encode('utf-8')

        headers = {
            'Api-Key': self.connect_key.encode('utf-8'),
            'Api-Sign': base64.b64encode(hex_output).decode('utf-8'),
            'Api-Nonce': nonce,
            'Accept': "application/json",
            'Content-Type': "application/x-www-form-urlencoded",
        }

        return headers

