import pandas as pd



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

    def crawlCandle(self) -> pd.DataFrame:
        """

        :return: api 콜을 진행해서 값을 가져온다.
        """
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

        result: [Candlestick] = request_client.get_candlestick_data(symbol="BTCUSDT", interval=CandlestickInterval.MIN1,
                                                                    startTime=None, endTime=None, limit=500)
        df = pandas.DataFrame([vars(s) for s in result])
        return df
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

        printDataAsGraph(df.tail(90))
        executeBacktest(df)