if __name__ == '__main__':

    from binance_f import RequestClient
    from binance_f.model import *
    from binance_f.constant.test import *
    from binance_f.base.printobject import *

    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

    result = request_client.get_candlestick_data(symbol="BTCUSDT", interval=CandlestickInterval.MIN1,
                                                 startTime=None, endTime=None, limit=10)

    print("======= Kline/Candlestick Data =======")
    PrintMix.print_data(result)
    print("======================================")
    from binance_f import RequestClient
    from binance_f.constant.test import *
    from binance_f.base.printobject import *
    from binance_f.model.constant import *

    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    result = request_client.get_balance_v2()
    PrintMix.print_data(result)
from binance_f import RequestClient
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.candlestickevent import Candlestick
import pandas
from datetime import datetime
import talib
import numpy as np


def printDataAsGraph(df: pandas.DataFrame):
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    fig = plt.figure(figsize=(8, 5))
    fig.set_facecolor('w')
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
    axes = []
    axes.append(plt.subplot(gs[0]))
    axes.append(plt.subplot(gs[1], sharex=axes[0]))
    axes[0].get_xaxis().set_visible(False)
    from mpl_finance import candlestick_ohlc

    x = np.arange(len(df.index))
    ohlc = df[['open', 'high', 'low', 'close']].astype(int).values
    dohlc = np.hstack((np.reshape(x, (-1, 1)), ohlc))

    # 봉차트
    candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b')

    # 이동평균선 그리기
    # axes[0].plot(index, kospi_df['MA3'], label='MA3', linewidth=0.7)
    # axes[0].plot(index, kospi_df['MA5'], label='MA5', linewidth=0.7)
    axes[0].plot(x, df['ema12'], label='ema12', linewidth=0.7)
    axes[0].plot(x, df['ema26'], label='ema26', linewidth=0.7)

    # 거래량 차트
    print(df['volume'])
    axes[1].bar(x, df['volume'], color='k', width=0.6, align='center')
    import datetime
    _xticks = []
    _xlabels = []
    _wd_prev = 0
    for _x, d in zip(x, df.openTime.values):
        weekday = pandas.to_datetime(d).weekday()
        if weekday <= _wd_prev:
            _xticks.append(_x)
            _xlabels.append(pandas.to_datetime(d).strftime('%m/%d'))
        _wd_prev = weekday
    axes[1].set_xticks(_xticks)
    axes[1].set_xticklabels(_xlabels, rotation=45, minor=False)
    plt.tight_layout()
    plt.show()
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG
from backtesting import Strategy, Backtest
from backtesting.lib import resample_apply
import pandas as pd

class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            # if self.position.is_short:
            #     self.()
            self.buy()
        elif crossover(self.ma2, self.ma1):
            # if self.position.is_long:
            #     self.position.close()
            self.sell()

def executeBacktest(data: pandas.DataFrame):
    data = data.set_index('openTime')
    data['Open'] = data['open']
    data['High'] = data['high']
    data['Low'] = data['low']
    data['Close'] = data['close']
    data['Volume'] = data['volume']
    bt = Backtest(data, SmaCross,
                  cash=100000000000, commission=.002, exclusive_orders=True)

    print(bt.run())
    bt.plot()
def printCandle():
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

    result: [Candlestick] = request_client.get_candlestick_data(symbol="BTCUSDT", interval=CandlestickInterval.MIN1,
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
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
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

    printDataAsGraph(df.tail(90))
    executeBacktest(df)


if __name__ == '__main__':
    printCandle()
