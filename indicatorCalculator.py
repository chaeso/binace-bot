from abc import *
import pandas as pd
import talib
import plotly.graph_objects as go
from backtest import TradeRecord


class GraphInfo:
    graphData: go
    attachToMainChart: bool

    def __init__(self, grpahData: go, attachToMainChart: bool):
        self.graphData = grpahData
        self.attachToMainChart = attachToMainChart


class BaseIndicatorBuilder(metaclass=ABCMeta):
    """
       지표들을 만드는 베이스 클래스.
    """
    _name: str

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        """
        지표들의 이름을 리턴한다.
        :return: 지표명
        """
        return self._name

    @abstractmethod
    def build_indicator(self, df: pd.DataFrame):
        """
        데이터를 바탕으로 지표를 빌드한다.
        :param df: 데티어
        :return: void
        """
        pass

    @abstractmethod
    def draw_graph(self, df: pd.DataFrame) -> [GraphInfo]:
        """
        데이터를 그린다.
        :param df: 데이터
        :return: trace 추가할 오브젝트 리
        """
        pass

    @abstractmethod
    def numberOfRows(self) -> int:
        """
        그래프를 그릴 때 필요한 추가 rows를 반환한다.
        :return:
        """


class RSIBuilder(BaseIndicatorBuilder):
    """
        RSI를 계산해 반환한다.
    """
    _days: int

    def __init__(self, days: int):
        name: str = "RSI" + str(days)
        super().__init__(name=name)
        self._days = days

    def build_indicator(self, df: pd.DataFrame):
        close = df['close']
        df[self.name] = talib.RSI(close, self._days)

    def numberOfRows(self) -> int:
        return 1

    def draw_graph(self, df: pd.DataFrame) -> [GraphInfo]:
        fig = go.Scatter(x=df['openTime'], y=df[self.name],
                         mode='lines',
                         name=self.name)
        return [GraphInfo(
            grpahData=fig,
            attachToMainChart=False
        )]


class SMABuilder(BaseIndicatorBuilder):
    """
    SMA를 계산해 반환한다.
    """
    _days: int

    def __init__(self, days: int):
        name: str = "SMA" + str(days)
        super().__init__(name=name)
        self._days = days

    def build_indicator(self, df: pd.DataFrame):
        close = df['close']
        df[self.name] = talib.SMA(close, self._days)


class EMABuilder(BaseIndicatorBuilder):
    """
    EMA를 계산해 반환한다.
    """
    _days: int

    def __init__(self, days: int):
        name: str = "EMA" + str(days)
        super().__init__(name=name)
        self._days = days

    def build_indicator(self, df: pd.DataFrame):
        close = df['close']
        df[self.name] = talib.EMA(close, self._days)

    def numberOfRows(self) -> int:
        return 0

    def draw_graph(self, df: pd.DataFrame) -> [GraphInfo]:
        fig = go.Scatter(x=df['openTime'], y=df[self.name],
                         mode='lines',
                         name=self.name)
        return [GraphInfo(
            grpahData=fig,
            attachToMainChart=True
        )]


class TTMSqueezeBuilder(BaseIndicatorBuilder):
    """
    TTM lazyBear Squeeze를 계산해 반환한다.
    https://github.com/hackingthemarkets/ttm-squeeze/blob/master/squeeze.py
    """

    def __init__(self):
        name: str = "TTM"
        super().__init__(name=name)

    def build_indicator(self, df: pd.DataFrame):
        close = df['close']
        df['20sma'] = close.rolling(window=20).mean()
        df['stddev'] = close.rolling(window=20).std()
        df['lower_band'] = df['20sma'] - (2 * df['stddev'])
        df['upper_band'] = df['20sma'] + (2 * df['stddev'])

        df['TR'] = abs(df['high'] - df['low'])
        df['ATR'] = df['TR'].rolling(window=20).mean()

        df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
        df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

        def in_squeeze(df):
            return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

        def off_squeeze(df):
            return df['lower_band'] < df['lower_keltner'] and df['upper_band'] > df['upper_keltner']

        df['squeeze_on'] = df.apply(in_squeeze, axis=1)

        df['squeeze_off'] = df.apply(off_squeeze, axis=1)

        # df['no_squeeze'] = (df['squeeze_on'] == False) and (df['squeeze_off'] == False)

        # if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        #     print("{} is coming out the squeeze".format(symbol))
        av = (df['high'].rolling(window=20).max() + df['low'].rolling(window=20).min()) / 2
        minus = (av + df['20sma']) / 2
        df['TTM'] = df['close'] - minus

    def numberOfRows(self) -> int:
        return 3

    def draw_graph(self, df: pd.DataFrame) -> [GraphInfo]:
        upper_band = go.Scatter(x=df['openTime'], y=df['upper_band'], name='Upper Bollinger Band',
                                line={'color': 'red'})
        lower_band = go.Scatter(x=df['openTime'], y=df['lower_band'], name='Lower Bollinger Band',
                                line={'color': 'red'})

        upper_keltner = go.Scatter(x=df['openTime'], y=df['upper_keltner'], name='Upper Keltner Channel',
                                   line={'color': 'blue'})
        lower_keltner = go.Scatter(x=df['openTime'], y=df['lower_keltner'], name='Lower Keltner Channel',
                                   line={'color': 'blue'})
        ttm = go.Scatter(x=df['openTime'], y=df['TTM'], name='TTM',
                         line={'color': 'blue'})
        graphs = [upper_band, lower_band, upper_keltner, lower_keltner]
        infos = list(map(lambda graph: GraphInfo(grpahData=graph, attachToMainChart=True), graphs))

        squeeze = go.Scatter(x=df['openTime'], y=df['squeeze_on'], name='squeeze_on',
                             line={'color': 'blue'})
        squeeze_off = go.Scatter(x=df['openTime'], y=df['squeeze_off'], name='squeeze_off',
                                 line={'color': 'red'})
        return [
            GraphInfo(grpahData=ttm, attachToMainChart=False),
            GraphInfo(grpahData=squeeze, attachToMainChart=False),
            GraphInfo(grpahData=squeeze_off, attachToMainChart=False)
        ]


class TradesIndicatorBuilder(BaseIndicatorBuilder):
    tradeRecords: [TradeRecord]

    def __init__(self, tradeRecords: [TradeRecord]):
        self.tradeRecords = tradeRecords
        name: str = "TRADES"
        super().__init__(name=name)

    def numberOfRows(self) -> int:
        return 0

    def build_indicator(self, df: pd.DataFrame):
        return

    def draw_graph(self, df: pd.DataFrame) -> [GraphInfo]:

        graphInfos: [GraphInfo] = []
        for tradeRecord in self.tradeRecords:
            if tradeRecord.is_long:
                graph = go.Scatter(
                    x=[tradeRecord.buy_date, tradeRecord.sell_date],
                    y=[tradeRecord.buy_coin_price, tradeRecord.sell_coin_price],
                    name='trade_long',
                    line={'color': 'red'}
                )
            else:
                graph = go.Scatter(
                    x=[tradeRecord.buy_date, tradeRecord.sell_date],
                    y=[tradeRecord.buy_coin_price, tradeRecord.sell_coin_price],
                    name='trade_short',
                    line={'color': 'blue'}
                )
            graphInfo = GraphInfo(
                grpahData=graph,
                attachToMainChart=True
            )
            graphInfos.append(graphInfo)
        return graphInfos


class AssetIndicatorBuilder(BaseIndicatorBuilder):

    def __init__(self):
        name: str = "asset"
        super().__init__(name=name)

    def numberOfRows(self) -> int:
        return 1

    def build_indicator(self, df: pd.DataFrame):
        return

    def draw_graph(self, df: pd.DataFrame) -> [GraphInfo]:
        fig = go.Scatter(x=df['openTime'], y=df[self.name],
                         mode='lines',
                         name=self.name)
        return [GraphInfo(
            grpahData=fig,
            attachToMainChart=False
        )]


class MACDIndicatorBuilder(BaseIndicatorBuilder):
    """
    MACD 지표를 계산한다.
    """
    _short: int
    _long: int
    _signal: int

    def __init__(self, short: int, long: int, signal: int):
        name: str = "MACD" + str(short) + '_' + str(long)
        super().__init__(name=name)
        self._short = short
        self._long = long
        self._signal = signal

    def numberOfRows(self) -> int:
        return 2

    def build_indicator(self, df: pd.DataFrame):
        macd, macdsignal, macdhist = talib.MACD(df['close'], self._short, self._long, )
        df['macd' + self.name] = macd
        df['macdsignal' + self.name] = macd
        df['macdhist' + self.name] = macdhist

    def draw_graph(self, df: pd.DataFrame) -> [GraphInfo]:
        fig = go.Scatter(x=df['openTime'], y=df['macdhist' + self.name],
                         mode='lines',
                         name=self.name)
        figsignal = go.Scatter(x=df['openTime'], y=df['macdsignal' + self.name],
                               mode='lines',
                               name=self.name)
        return [GraphInfo(grpahData=fig,
                          attachToMainChart=False),
                GraphInfo(
                    grpahData=figsignal,
                    attachToMainChart=False
                )
                ]
