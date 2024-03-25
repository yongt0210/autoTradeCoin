import pandas as pd
from pandas import DataFrame
from datetime import datetime

# 시간 포맷 
def timestamp_to_datetime(timestamp, interval='24h'):
    date = datetime.fromtimestamp(timestamp / 1000)

    if interval == '24h':
        return date.strftime('%Y-%m-%d')
    else:
        return date.strftime('%Y-%m-%d %H:%M:%S')

# 현재 시간 구하기
def get_now_time(format='%Y-%m-%d %H:%M:%S'):
    now = datetime.now()

    return now.strftime(format)

# 볼린저 밴드 구하기 함수
def calculate_bollinger_bands(df, window_size, std):
    rolling_mean = df['close'].rolling(window=window_size).mean()
    rolling_std = df['close'].rolling(window=window_size).std()

    upper_band = rolling_mean + (rolling_std * std)
    lower_band = rolling_mean - (rolling_std * std)

    return rolling_mean, upper_band, lower_band

# 데이터프레임으로 만들기
def makeDataFrame(data, interval="24h"):
    df = DataFrame(data, columns=['datetime', 'open', 'close', 'high', 'low', 'volume'])
    df = df.set_index('datetime')

    df = df[['open', 'high', 'low', 'close', 'volume']]
    df = df.astype(float)

    df.index = pd.to_datetime(df.index, unit='ms', utc=True)

    df.index = df.index.tz_convert('Asia/Seoul')
    if interval == "24h":
        df.index = df.index.strftime('%Y-%m-%d')
    else:
        df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')

    return df

# 매수 시점 
def generate_signals(data, window=5, k=0.5):
    df = makeDataFrame(data)

    # 변동률
    df["range"] = df["high"] - df["low"]

    # 목표가
    df["target"] = df['open'] + (df['range'].shift(1) * k)

    # 이동평균선
    # df["mean"], df["upperBand"], df["lowerBand"] = calculate_bollinger_bands(df, window_size=window_size, std=std)
    df["mean"] = df["close"].rolling(window=window).mean()

    # 가격 비교
    df["diff"] = df["close"] - df["target"]

    # 이동평균선 위이고, 고가가 목표가보다 많으면(한번이라도 목표가를 돌파하면) 구매
    df = df[(df["close"] >= df["mean"]) & (df["high"] >= df["target"])]

    return df