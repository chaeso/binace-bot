from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.model import AccountInformationV2, MarkPrice
from binance_f.model.accountinformationv2 import PositionV2
from binance_f.model import OrderSide, OrderType
from binance_f.base.printobject import *
from binance_f.model.exchangeinformation import Symbol
import time
import numpy as np
from slack import SlackSender
class RealBot:
    """
    바이낸스에서 돌려가면서 계산을 한다.
    """

    callDelay: int


    availableBalance: float = 0.0
    unrealizedProfit: float = 0.0
    positionAmt: float = 0.0

    symbol: str
    leverage: int

    entryPrice: float = 0.0

    markPrice: float
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

    ## symbol info
    pricePrecision: int
    """
    pricePrecision = 5 일 경우 1.12856 같이 주문 가능
    """
    quantityPrecision: int
    """
    quantityPrecision = 0 일 경우 1, 2, 3... 같이 주문 가격 형성됨 
    """

    slackSender: SlackSender = SlackSender()

    def __init__(self, symbol: str, leverage: int):
        self.symbol = symbol
        self.leverage = leverage
        self.get_symbol_info()
        result = self.request_client.change_initial_leverage(symbol=self.symbol, leverage=self.leverage)
        print(result)

    def get_symbol_info(self):
        """
        현재 심볼의 정보를 가져온다.
        :return:
        """

        result = self.request_client.get_exchange_information()
        print("======= Exchange Information =======")
        print("timezone: ", result.timezone)
        print("serverTime: ", result.serverTime)
        print("=== Rate Limits ===")
        PrintMix.print_data(result.rateLimits)
        print("===================")
        print("=== Exchange Filters ===")
        PrintMix.print_data(result.exchangeFilters)
        print("===================")
        print("=== Symbols ===")
        PrintMix.print_data(result.symbols)
        symbols: [Symbol] = result.symbols
        for symbol in symbols:
            if symbol.symbol == self.symbol:
                self.pricePrecision = symbol.pricePrecision
                self.quantityPrecision = symbol.quantityPrecision
        print("===================")
        print("====================================")

    def refreshCurrentPrice(self):
        """
        시장가 긁어온다.
        :return:
        """
        result: MarkPrice = self.request_client.get_mark_price(symbol=self.symbol)
        self.markPrice = result.markPrice


    def refreshCurrentBudget(self):
        """
        현재 잔고를 파악한다.
        :return:
        """

        result: AccountInformationV2 = self.request_client.get_account_information_v2()

        print(result)
        self.availableBalance = result.availableBalance
        positions: [PositionV2] = result.positions
        for position in positions:
            if position.symbol == self.symbol:
                self.leverage = position.leverage
                self.positionAmt = position.positionAmt
                self.entryPrice = position.entryPrice


    def refreshCurrentTrade(self):
        """
        종료되지 않은 계약을 갱신한다.
        :return:
        """
        pass

    def get_max_pos_size_ito_usdt(self, symbol: str, leverage: int) -> float:
        if symbol == 'BTCUSDT':
            kvs = [(100, 50000), (50, 250000), (20, 1000000), (10, 5000000), (5, 20000000),
                   (4, 50000000), (3, 100000000), (2, 200000000)]
        elif symbol == 'ETHUSDT':
            kvs = [(75, 10000), (50, 100000), (25, 500000), (10, 1000000), (5, 2000000),
                   (4, 5000000), (3, 10000000), (2, 20000000)]
        elif symbol in ['ADAUSDT', 'BNBUSDT', 'DOTUSDT', 'EOSUSDT', 'ETCUSDT', 'LINKUSDT', 'LTCUSDT',
                        'TRXUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'XTZUSDT', 'BCHUSDT']:
            kvs = [(50, 10000), (25, 50000), (10, 250000), (5, 1000000), (4, 2000000),
                   (3, 5000000), (2, 10000000)]
        elif symbol in ['AAVEUSDT', 'ALGOUSDT', 'ALPHAUSDT', 'ATOMUSDT', 'AVAXUSDT', 'AXSUSDT',
                        'BALUSDT', 'BANDUSDT', 'BATUSDT', 'BELUSDT', 'BLZUSDT', 'BZRXUSDT', 'COMPUSDT',
                        'CRVUSDT', 'CVCUSDT', 'DASHUSDT', 'DEFIUSDT', 'DOGEUSDT', 'EGLDUSDT', 'ENJUSDT',
                        'FILUSDT', 'FLMUSDT', 'FTMUSDT', 'HNTUSDT', 'ICXUSDT', 'IOSTUSDT', 'IOTAUSDT',
                        'KAVAUSDT', 'KNCUSDT', 'KSMUSDT', 'LRCUSDT', 'MATICUSDT', 'MKRUSDT', 'NEARUSDT',
                        'NEOUSDT', 'OCEANUSDT', 'OMGUSDT', 'ONTUSDT', 'QTUMUSDT', 'RENUSDT', 'RLCUSDT',
                        'RSRUSDT', 'RUNEUSDT', 'SNXUSDT', 'SOLUSDT', 'SRMUSDT', 'STORJUSDT',
                        'SUSHIUSDT', 'SXPUSDT', 'THETAUSDT', 'TOMOUSDT', 'TRBUSDT', 'UNIUSDT',
                        'VETUSDT', 'WAVESUSDT', 'YFIIUSDT', 'YFIUSDT', 'ZECUSDT', 'ZILUSDT', 'ZRXUSDT',
                        'ZENUSDT', 'SKLUSDT', 'GRTUSDT', '1INCHUSDT']:
            kvs = [(20, 5000), (10, 25000), (5, 100000), (2, 250000), (1, 1000000)]
        elif symbol in ['CTKUSDT']:
            kvs = [(10, 5000), (5, 25000), (4, 100000), (2, 250000), (1, 1000000)]
        else:
            raise Exception(f'{symbol} unknown symbol')
        for kv in kvs:
            if leverage > kv[0]:
                return kv[1]
        return 9e12

    def getMaximumBuyable(self) -> float:
        """
        현재 가격으로 살 수 있는 최대 값을 구한다.

        :return:
        """
        max_pos: float = self.get_max_pos_size_ito_usdt(self.symbol, self.leverage) / self.markPrice
        amount: float = self.availableBalance / self.markPrice * self.leverage


        def trunc(values, decs=0):
            return np.trunc(values * 10 ** decs) / (10 ** decs)
        return trunc(np.min([amount * 0.90, max_pos]), decs=self.quantityPrecision)

    def orderBuy(self):
        """
        계약을 체결한다.
        :return: 현재 잔고
        """

        self.refreshCurrentBudget()
        self.refreshCurrentPrice()
        amount = self.getMaximumBuyable()
        result = self.request_client.post_order(symbol=self.symbol, side=OrderSide.BUY, ordertype=OrderType.MARKET,
                                           quantity=amount, positionSide="BOTH")


    def closeBuy(self):
        """
        계약을 종료한다.
        :return:
        """

        self.refreshCurrentBudget()
        self.refreshCurrentPrice()
        size = self.positionAmt
        print(size)
        if size > 0:
            result = self.request_client.post_order(symbol=self.symbol, side=OrderSide.SELL, ordertype=OrderType.MARKET,
                                                    quantity=size, positionSide="BOTH", reduceOnly=True)

    def orderSell(self):
        """
        숏 계약을 체결한다.
        :return:
        """
        self.refreshCurrentBudget()
        self.refreshCurrentPrice()
        amount = self.getMaximumBuyable()
        result = self.request_client.post_order(symbol=self.symbol, side=OrderSide.SELL, ordertype=OrderType.MARKET,
                                                quantity=amount, positionSide="BOTH")


    def closeSell(self):
        """
        숏 계약을 종결한다.
        :return:
        """

        self.refreshCurrentBudget()
        self.refreshCurrentPrice()
        size = self.positionAmt
        print(size)
        if size < 0:
            result = self.request_client.post_order(symbol=self.symbol, side=OrderSide.BUY, ordertype=OrderType.MARKET,
                                                    quantity=-size, positionSide="BOTH", reduceOnly=True)


if __name__ == '__main__':

    bot = RealBot(symbol="BTCUSDT", leverage=1)

    while True:

        time.sleep(1)
        bot.refreshCurrentPrice()
        bot.refreshCurrentBudget()
        bot.slackSender.send_message(f'현재 가격 {bot.markPrice}, 잔고 {bot.availableBalance}')

