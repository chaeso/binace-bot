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

    def notifyByTelegram(self):
        """
        텔레그램이나 슬랙으로 정보를 보낸다.
        :return:
        """