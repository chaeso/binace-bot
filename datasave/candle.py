from binance_f import RequestClient
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.candlestickevent import Candlestick
import pandas
from datetime import datetime
import talib
import numpy as np

def printCandle():
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

    result: [Candlestick] = request_client.get_candlestick_data(symbol="BTCUSDT", interval=CandlestickInterval.DAY1,
                                      startTime=None, endTime=None, limit=500)
    # np = numpy.vectorize(result)
    # print(np)
    # df = pandas.DataFrame(data=np, columns=['startTime', ])
    # print(df)
    df = pandas.DataFrame([vars(s) for s in result])
    print(df)
    print(df['openTime'])
    df['openTime'] = [datetime.fromtimestamp(x//1000.0) for x in df['openTime']]
    df['closeTime'] = [datetime.fromtimestamp(x // 1000.0) for x in df['closeTime']]
    df['close'] = df['close'].astype(float)
    print(df)

    close = np.array(df['close'])
    print(close)
    df['sma5'] = talib.SMA(close, 5)
    df['sma20'] = talib.SMA(close, 20)
    df['sma120'] = talib.SMA(close, 120)

    df['ema12'] = talib.EMA(close, 12)
    df['ema26'] = talib.EMA(close, 26)
    df['rsi14'] = talib.RSI(close, 14)

    macd, macdsignal, macdhist = talib.MACD(close, 12, 26, 9)

    df['macd'] = macd
    print(df)
    df.to_excel("output.xlsx")


if __name__ == '__main__':
    printCandle()