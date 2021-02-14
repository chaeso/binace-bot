# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from typing import Any


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

class CandleStickData:
    openTime: int
    open: float
    high: float
    low: float
    close: float
    volumn: float
    closeTime: int
    qouteAssetVolume: float
    numberOfTrades: int
    takerBuyBaseAssetVolume: float
    takerBuyQuoteAssetVolume: float

    def __init__(self, obj: Any) -> None:
        pass




# Press the green button in the gutter to run the script.
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