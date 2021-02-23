from sqlalchemy import Column, Integer, DECIMAL, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DATETIME
Base = declarative_base()
class OrderBookORM(Base):
    """
    주문창의 비드, 애스크를 ORM 형태로 저장한다.
    """
    __tablename__ = "order_book_v2"

    id = Column(Integer, primary_key=True)
    """
        심볼명
    """
    symbol = Column(String(20))
    """
        체결시간
    """
    time = Column(DATETIME(fsp=6))
    """
        비드들 가격
    """
    bid_0_price = Column(DECIMAL(18, 8))
    bid_0_qty = Column(DECIMAL(18, 8))
    bid_1_price = Column(DECIMAL(18, 8))
    bid_1_qty = Column(DECIMAL(18, 8))
    bid_2_price = Column(DECIMAL(18, 8))
    bid_2_qty = Column(DECIMAL(18, 8))
    bid_3_price = Column(DECIMAL(18, 8))
    bid_3_qty = Column(DECIMAL(18, 8))
    bid_4_price = Column(DECIMAL(18, 8))
    bid_4_qty = Column(DECIMAL(18, 8))
    bid_5_price = Column(DECIMAL(18, 8))
    bid_5_qty = Column(DECIMAL(18, 8))
    bid_6_price = Column(DECIMAL(18, 8))
    bid_6_qty = Column(DECIMAL(18, 8))
    bid_7_price = Column(DECIMAL(18, 8))
    bid_7_qty = Column(DECIMAL(18, 8))
    bid_8_price = Column(DECIMAL(18, 8))
    bid_8_qty = Column(DECIMAL(18, 8))
    bid_9_price = Column(DECIMAL(18, 8))
    bid_9_qty = Column(DECIMAL(18, 8))
    bid_18_price = Column(DECIMAL(18, 8))
    bid_18_qty = Column(DECIMAL(18, 8))
    bid_11_price = Column(DECIMAL(18, 8))
    bid_11_qty = Column(DECIMAL(18, 8))
    bid_12_price = Column(DECIMAL(18, 8))
    bid_12_qty = Column(DECIMAL(18, 8))
    bid_13_price = Column(DECIMAL(18, 8))
    bid_13_qty = Column(DECIMAL(18, 8))
    bid_14_price = Column(DECIMAL(18, 8))
    bid_14_qty = Column(DECIMAL(18, 8))
    bid_15_price = Column(DECIMAL(18, 8))
    bid_15_qty = Column(DECIMAL(18, 8))
    bid_16_price = Column(DECIMAL(18, 8))
    bid_16_qty = Column(DECIMAL(18, 8))
    bid_17_price = Column(DECIMAL(18, 8))
    bid_17_qty = Column(DECIMAL(18, 8))
    bid_18_price = Column(DECIMAL(18, 8))
    bid_18_qty = Column(DECIMAL(18, 8))
    bid_19_price = Column(DECIMAL(18, 8))
    bid_19_qty = Column(DECIMAL(18, 8))

    ask_0_price = Column(DECIMAL(18, 8))
    ask_0_qty = Column(DECIMAL(18, 8))
    ask_1_price = Column(DECIMAL(18, 8))
    ask_1_qty = Column(DECIMAL(18, 8))
    ask_2_price = Column(DECIMAL(18, 8))
    ask_2_qty = Column(DECIMAL(18, 8))
    ask_3_price = Column(DECIMAL(18, 8))
    ask_3_qty = Column(DECIMAL(18, 8))
    ask_4_price = Column(DECIMAL(18, 8))
    ask_4_qty = Column(DECIMAL(18, 8))
    ask_5_price = Column(DECIMAL(18, 8))
    ask_5_qty = Column(DECIMAL(18, 8))
    ask_6_price = Column(DECIMAL(18, 8))
    ask_6_qty = Column(DECIMAL(18, 8))
    ask_7_price = Column(DECIMAL(18, 8))
    ask_7_qty = Column(DECIMAL(18, 8))
    ask_8_price = Column(DECIMAL(18, 8))
    ask_8_qty = Column(DECIMAL(18, 8))
    ask_9_price = Column(DECIMAL(18, 8))
    ask_9_qty = Column(DECIMAL(18, 8))
    ask_18_price = Column(DECIMAL(18, 8))
    ask_18_qty = Column(DECIMAL(18, 8))
    ask_11_price = Column(DECIMAL(18, 8))
    ask_11_qty = Column(DECIMAL(18, 8))
    ask_12_price = Column(DECIMAL(18, 8))
    ask_12_qty = Column(DECIMAL(18, 8))
    ask_13_price = Column(DECIMAL(18, 8))
    ask_13_qty = Column(DECIMAL(18, 8))
    ask_14_price = Column(DECIMAL(18, 8))
    ask_14_qty = Column(DECIMAL(18, 8))
    ask_15_price = Column(DECIMAL(18, 8))
    ask_15_qty = Column(DECIMAL(18, 8))
    ask_16_price = Column(DECIMAL(18, 8))
    ask_16_qty = Column(DECIMAL(18, 8))
    ask_17_price = Column(DECIMAL(18, 8))
    ask_17_qty = Column(DECIMAL(18, 8))
    ask_18_price = Column(DECIMAL(18, 8))
    ask_18_qty = Column(DECIMAL(18, 8))
    ask_19_price = Column(DECIMAL(18, 8))
    ask_19_qty = Column(DECIMAL(18, 8))


if __name__ == '__main__':
    """
    DB에 trade 관련 테이블을 추가한다.
    """
    orm = OrderBookORM()
    from db import engine
    Base.metadata.create_all(engine)