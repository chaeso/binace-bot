from abc import *
import pandas as pd
import talib

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
        데이터를 바탕으로 지표를 빌드하낟.
        :param df: 데티어
        :return: void
        """
        pass


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

        df['squeeze_on'] = df.apply(in_squeeze, axis=1)

        if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
            print("{} is coming out the squeeze".format(symbol))
