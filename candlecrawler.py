import pandas as pd
from binance_f import RequestClient
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.candlestickevent import Candlestick
from datetime import datetime
from indicatorCalculator import *


class CandleCrawler:

    data_save_path = "output.xlsx"

    indiecatorBuilder: [BaseIndicatorBuilder]
    def saveToExcel(self, df: pd.DataFrame):
        """
            데이터를 저장한다.
        :param df: 저장할 데이터
        :return: void
        """
        df.to_excel(self.data_save_path)



    def addIndicator(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        데이터에 지표들을 추가한다.
        :param df:
        :return:
        """
        self.indiecatorBuilder = [
            EMABuilder(12),
            EMABuilder(26),
            RSIBuilder(14),
            SMABuilder(5),
            SMABuilder(20),
            SMABuilder(120),
            TTMSqueezeBuilder()
        ]

        for builder in self.indiecatorBuilder:
            builder.build_indicator(df)
        return df


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
        df['volume'] = df['volume'].astype(float)
        return df

    def intervalToMilliSeoncds(self, interval: CandlestickInterval) -> int:
        """
        인터벌을 밀리세컨드로 바꾼다.
        :param interval: 인터벌
        :return: 밀리세컨
        """
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
        단일 페이지를 바이낸스에서 크롤링한다.
        :param endTime: timestamp milli로 된 맨 마지막 시간
        :param limit: 캔들 수
        :param interval: 캔들간 간격
        :return: 페이
        """
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

        result: [Candlestick] = request_client.get_candlestick_data(symbol="BTCUSDT", interval=interval,
                                                                    startTime=None, endTime=endTime, limit=limit)
        df = pd.DataFrame([vars(s) for s in result])
        return df


    def crawlWithMultiplePage(self, page: int, limit: int, interval: CandlestickInterval):
        """
        여러 페이지를 가지고 크롤링한다.
        :param page: 가져올 페이지 수
        :param limit: 한 페이지 당 리미트 값
        :param interval: 캔들 봉 가격
        :return: 크롤링한 페이지
        """
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
        df = self.addIndicator(df)
        return df

    def validateData(
            self,
            path: str,
            page: int,
            limit: int,
            interval: CandlestickInterval
    ) -> bool:
        """
        하드에 있는 데이터가 실제로 적합한지 판단한다.
        :param path: 데이터 경로
        :param limit: 페이지당 수
        :param page: 페이지 수
        :param interval: 봉 간격
        :return: 적합한지 여부
        """
        df = pd.read_excel(path)
        if df is None:
            return False
        expectedColumns: int = page * limit
        if expectedColumns != len(df):
            return False

        expectedInterval: pd.Timedelta = pd.to_timedelta(self.intervalToMilliSeoncds(interval), unit="ms")
        currentInterval: pd.Timedelta = df['openTime'][1] - df['openTime'][0]
        if currentInterval != expectedInterval:
            return False

        return True

    def load_data(
            self,
            path: str,
            refresh: bool,
            page: int,
            limit: int,
            interval: CandlestickInterval
    ) -> pd.DataFrame:
        """
        내부 액셀에서 데이터를 가져오거나, 바이낸스에 api 요청을 해서 값을 가져온다.
        :param path: 내부 데이터 저장 공간
        :param refresh: refresh 인자가 True인 경우, 무조건 바이낸스에 새 값을 가져온다.
        :param limit: 페이지당 캔들 수
        :param page: 페이지 수
        :param interval: 간격
        :return: 데이터
        """
        if refresh:
            df = self.crawlWithMultiplePage(page = page, limit = limit, interval = interval)
            self.saveToExcel(df)
            return df
        if self.validateData(path, page= page, limit=limit, interval=interval):
            return pd.read_excel(path)
        else:
            df = self.crawlWithMultiplePage(page=page, limit=limit, interval=interval)
            self.saveToExcel(df)
            return df


if __name__ == '__main__':
    crawler = CandleCrawler()
    df = crawler.load_data(crawler.data_save_path, refresh=True, page= 1, limit=500, interval=CandlestickInterval.MIN1)

    print(df)
