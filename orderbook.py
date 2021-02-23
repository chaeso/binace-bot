import logging
from binance_f import SubscriptionClient
from binance_f.constant.test import *
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException

from binance_f.base.printobject import *
from binance_f.model import OrderBookEvent
from order_book_orm import OrderBookORM
from datetime import datetime
from db import session


def convertToOrderORM(orderBookEvent: OrderBookEvent) -> OrderBookORM:
    """
    오더북을 mysql에 저장하기 편한 매퍼로 변환한다.
    :param orderBookEvent: 소켓에서 내려오는 값들
    :return: mysql 매퍼
    """
    orm = OrderBookORM()
    orm.symbol = orderBookEvent.symbol
    orm.time = datetime.fromtimestamp(orderBookEvent.eventTime / 1000)
    for index, value in enumerate(orderBookEvent.asks):
        setattr(orm, 'ask_' + str(index) + '_price', value.price)
        setattr(orm, 'ask_' + str(index) + '_qty', value.qty)

    for index, value in enumerate(orderBookEvent.bids):
        setattr(orm, 'bid_' + str(index) + '_price', value.price)
        setattr(orm, 'bid_' + str(index) + '_qty', value.qty)

    return orm


def insertORM(orm: OrderBookORM):
    """
    sql 에 insert 연산을 한다.
    :param orm: orm mapping
    :return: void
    """
    session.add(
        orm
    )
    session.commit()
def callback(data_type: 'SubscribeMessageType', event: 'any'):
    """
    소켓 콜백을 받는다.
    :param data_type:
    :param event:
    :return:
    """

    if data_type == SubscribeMessageType.RESPONSE:
        pass
    elif  data_type == SubscribeMessageType.PAYLOAD:
        orm = convertToOrderORM(event)
        insertORM(orm)
       # sub_client.unsubscribe_all()

    else:
        print("Unknown Data:")
    print()



def error(e: 'BinanceApiException'):
    """
    에러를 처리한다.
    :param e:
    :return:
    """
    print(e.error_code + e.error_message)

def execute():
    """
    크롤링을 진행한다.
    :return:
    """


    logger = logging.getLogger("binance-futures")
    logger.setLevel(level=logging.CRITICAL)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key)



    sub_client.subscribe_book_depth_event("btcusdt", 20, callback, error, update_time=UpdateTime.FAST)

if __name__ == '__main__':
    execute()
