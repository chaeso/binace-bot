import pandas as pd
class PriceCalculator:

    def cal_current_price_short(
            self,
            dollar_budget: float,
            buy_price: float,
            current_price: float,
            leverage: int = 1,
            commission_percent: float = 0) -> float :
        """숏 포지션을 했을 때, 현재 매도했을 때 자산의 가격을 계산한다..

        Args:
            budget: 구매한 현금 달
            buy_price: 구매했을 때 자산의 시세
            current_price: 현재 자산의 시세
            leverage: 1배~125배의 가격
            commission_percent: 거래소에 지불하는 수수료
        Returns:
            현재 거래를 종료했을 때 자산의 가치
        """

        ## 홀드하고 있는 코인량 계산
        current_holding_coin: float = dollar_budget / buy_price

        return (1 + (buy_price - current_price) / buy_price) * dollar_budget

    def cal_current_price_long(
            self,
            dollar_budget: float,
            buy_price: float,
            current_price: float,
            leverage: int,
            commission_percent: float) -> float :
        """ 포지션을 했을 때, 현재 매도했을 때 자산의 가격을 계산한다.

        Args:
            dollar_budget:
            buy_price: 구매했을 때 자산의 시세
            current_price: 현재 자산의 시세
            leverage: 1배~125배의 가격
            commission_percent: 거래소에 지불하는 수수료
        Returns:
            현재 거래를 종료했을 때 자산의 가
        """

        return current_price / buy_price * dollar_budget

class CandleCrawler:
    """
        LIMIT 이 500까지밖에 안 되므로, 여러번 api를 콜하며 다량 캔들스틱을 가져온다.
    """
    def crawl_candlestick(self, limit: int):
        pass
class Trade:
    """
    현재 등록중인 거래
    """
    """
        구매 당시 코인 가격
    """
    initial_coin_price: float
    """
        구매 당시 구입한 재화
    """
    initial_dollars: float
    """
        포지션
    """
    is_long: bool


    """
        청산 여부
    """
    def is_closed(self) -> bool:
        return False

    """
       지금 거래를 종료했을 경우, 현제 가격을 리턴한다.
    """
    def current_dollars(self, coin_price: float) -> float:
        return 0


class BackTestRecorder:


    def draw_complete_trade(self, trade: Trade):
        pass

    def draw_candlesticks(self):
        pass

class BackTest:
    """
    백테스트 과정
    Args:
        initial_budget: 최초 투자 잔고
        chart: 캔들스틱
        current_trades: 현재 종료되지 않은 거래들
        current_budget: float 현재 종료된 거래
    """

    initial_budget: float

    chart: pd.DataFrame
    current_trades: [Trade]


    current_budget: float
    def simulate(self):

        turn_length: int = 0

        for turn in range(0, turn_length):
            self.clear_turn(turn)



    def clear_turn(self, turn: int):
        current_price = chart[turn]
        for trade in current_price:
            if trade.is_closed():
                self.close_trade(trade)

        return


    def should_buy_long(self) -> bool:
        """
        롱 매수를 해야하는 지 판단
        :return: 롱 매수를 해야 하는지 여부
        """
    def should_buy_short(self) -> bool:
        """
        숏 매수를 해야 하는 지 판단
        :return: 숏 매수를 해야 하는지 여부
        """

    def should_sell_long(self) -> bool:
        """
        보유한 롱 계약을 끝내야 하는지 판단
        :return:
        """

    def should_sell_short(self) -> bool:
        pass




    def close_trade(self, trade: Trade):
        pass

if __name__ == '__main__':
    priceCalulator = PriceCalculator()

    print(priceCalulator.cal_current_price_short(
        dollar_budget=1,
        buy_price=1000,
        current_price=900
    ))


    print(priceCalulator.cal_current_price_short(
        dollar_budget=1,
        buy_price=1000,
        current_price=1100
    ))