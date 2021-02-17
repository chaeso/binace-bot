class RealBot:
    """
    바이낸스에서 돌려가면서 계산을 한다.
    """

    callDelay: int

    def refreshCurrentPrice(self):
        """
        캔들을 긁어온다.
        :return:
        """
        pass


    def refreshCurrentBudget(self):
        """
        현재 잔고를 파악한다.
        :return:
        """
        pass
    def refreshCurrentTrade(self):
        """
        종료되지 않은 계약을 갱신한다.
        :return:
        """
        pass

    def orderBuy(self):
        """
        계약을 체결한다.
        :return:
        """

    def closeBuy(self):
        """
        계약을 종료한다.
        :return:
        """
        pass

    def notifyByTelegram(self):
        """
        텔레그램이나 슬랙으로 정보를 보낸다.
        :return:
        """
        pass

if __name__ == '__main__':
    from binance_f import RequestClient
    from binance_f.constant.test import *
    from binance_f.base.printobject import *
    from binance_f.model.constant import *

#     request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
#     result = request_client.get_all_orders(symbol="DOTUSDT")
#     PrintMix.print_data(result)
#     request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
#     result = request_client.get_order(symbol="DOTUSDT", orderId=3025899771)
#     PrintBasic.print_obj(result)
#     # request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
#     # result = request_client.cancel_order(symbol="DOTUSDT", orderId=3026316451)
#     # PrintBasic.print_obj(result)
#     request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
# #     # result = request_client.post_order(symbol="DOTUSDT", side=OrderSide.SELL, ordertype=OrderType.STOP_MARKET,
# #     #                                     quantity=0.9, closePosition=True, stopPrice=30.657result = request_client.post_order(symbol="BTCUSDT", side=OrderSide.SELL, ordertype=OrderType.STOP_MARKET, stopPrice=8000.1, closePosition=True, positionSide="LONG")
# #
#     result = request_client.post_order(symbol="DOTUSDT", side=OrderSide.BUY, ordertype=OrderType.MARKET,
#                                        quantity=2.9, positionSide="BOTH")
# #     #
#
#     # request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
#     # result = request_client.get_position_v2()
#     # PrintMix.print_data(result)
#
#
# .
#     from binance_f import RequestClient
#     from binance_f.constant.test import *
#     from binance_f.base.printobject import *
#     from binance_f.model.constant import *
#
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    result = request_client.get_account_information_v2()
#     from binance_f import RequestClient
#     from binance_f.constant.test import *
#     from binance_f.base.printobject import *
#     from binance_f.model.constant import *
#
    # request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    # result = request_client.get_balance_v2()
    # PrintMix.print_data(result)
#     request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
#     result = request_client.get_position()
#     PrintMix.print_data(result)
#     request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
#     result = request_client.get_leverage_bracket()
#     PrintMix.print_data(result)
