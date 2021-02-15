import pandas as pd
from binance_f import RequestClient
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.candlestickevent import Candlestick
import pandas
from datetime import datetime
import talib
import numpy as np



class CandleCrawler:

    def saveToExcel(self, data: pd.DataFrame):
        print(df)
        df.to_excel("output.xlsx")



    def addIndicator(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        데이터에 지표들을 추가한다.
        :param df:
        :return:
        """
        df['sma5'] = talib.SMA(close, 5)
        df['sma20'] = talib.SMA(close, 20)
        df['sma120'] = talib.SMA(close, 120)

        df['ema12'] = talib.EMA(close, 12)
        df['ema26'] = talib.EMA(close, 26)
        df['rsi14'] = talib.RSI(close, 14)

        macd, macdsignal, macdhist = talib.MACD(close, 12, 26, 9)

        df['macd'] = macd

        printDataAsGraph(df.tail(90))
        executeBacktest(df)
        pass


    def convertDefaultData(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        크롤링한 데이터의 형변환 등을 진행한다.
        :param df: 크롤링만 한 데이터
        :return: 변환한 데이터
        """
        df['openTime'] = [datetime.fromtimestamp(x // 1000.0) for x in df['openTime']]
        df['closeTime'] = [datetime.fromtimestamp(x // 1000.0) for x in df['closeTime']]
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        return df

    def intervalToMilliSeoncds(self, interval: CandlestickInterval) -> int:
        if interval == CandlestickInterval.MIN1:
            return 60000
        if interval == CandlestickInterval.MIN3:
            return 60000 * 3
        if interval == CandlestickInterval.MIN5:
            return 60000 * 5
        if interval == CandlestickInterval.MIN15:
            return 60000 * 15
        if interval == CandlestickInterval.MIN30:
            return 60000 * 30
        if interval == CandlestickInterval.HOUR1:
            return 3600000
        if interval == CandlestickInterval.HOUR2:
            return 3600000 * 2
        if interval == CandlestickInterval.HOUR4:
            return 3600000 * 4
        if interval == CandlestickInterval.HOUR6:
            return 3600000 * 6
        if interval == CandlestickInterval.HOUR8:
            return 3600000 * 8
        if interval == CandlestickInterval.HOUR12:
            return 3600000 * 12
        if interval == CandlestickInterval.DAY1:
            return 3600000 * 24
        if interval == CandlestickInterval.DAY3:
            return 3600000 * 24 * 3
        if interval == CandlestickInterval.WEEK1:
            return 3600000 * 24 * 7
        if interval == CandlestickInterval.MON1:
            return 3600000 * 24 * 30
        return None
    def crawlCandle(self, endTime: int, limit: int, interval: CandlestickInterval) -> pd.DataFrame:
        """

        :return: api 콜을 진행해서 값을 가져온다.
        """
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

        result: [Candlestick] = request_client.get_candlestick_data(symbol="BTCUSDT", interval=interval,
                                                                    startTime=None, endTime=endTime, limit=limit)
        df = pd.DataFrame([vars(s) for s in result])
        return df


    def crawlWithMultiplePage(self, page: int, limit: int, interval: CandlestickInterval):

        lastEndTime: int = None

        df = []
        for i in range(0, page):
            if lastEndTime is None:
                df = self.crawlCandle(lastEndTime, limit, interval)
            else:
                currentPage = self.crawlCandle(lastEndTime, limit, interval)
                df = pd.concat([currentPage, df], ignore_index=True)
            lastEndTime = df.loc[0]['openTime'] - self.intervalToMilliSeoncds(interval)
        df = self.convertDefaultData(df)
        return df

if __name__ == '__main__':
    crawler = CandleCrawler()
    df = crawler.crawlWithMultiplePage(2, 10, CandlestickInterval.MIN1)
    print(df)
    crawler.saveToExcel(df)