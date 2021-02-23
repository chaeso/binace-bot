
from db import engine, session
from order_book_orm import OrderBookORM
import pandas as pd
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from candlecrawler import *

class OrderBookExporter:
    data_save_path = "exporter_output.xlsx"

    def saveToExcel(self, df: pd.DataFrame):
        """
            데이터를 저장한다.
        :param df: 저장할 데이터
        :return: void
        """
        col = ['time']
        for index in range(0, 20):
            if index == 10:
                continue
            col.append('ask_' + str(index) + '_price')
            col.append('ask_' + str(index) + '_qty')
        for index in range(0, 20):
            if index == 10:
                continue
            col.append('bid_' + str(index) + '_price')
            col.append('bid_' + str(index) + '_qty')
        df.to_excel(self.data_save_path, columns=col)

    def get_total(self) -> int:
        return session.query(OrderBookORM).count()

    def get_orms(self, limit: int, offset: int) -> [OrderBookORM]:
        return session.query(OrderBookORM).order_by('time').limit(limit).offset(offset).all()

    def convert_to_pandas(self, orms: [OrderBookORM]):
        return pd.DataFrame([vars(s) for s in orms])

    def export_all(self):
        count = self.get_total()

        datas:[OrderBookORM] = []

        total_page = 100
        limit = 1000
        for i in range(30, total_page):
            offset = limit * i
            datas += self.get_orms(limit, offset)
            print(i)
        df = self.convert_to_pandas(datas)
        df = self.retreat(df)
        self.saveToExcel(df)

    def read_from_excel(self):
        return pd.read_excel(self.data_save_path)

    def retreat(self, df: pd.DataFrame):
        for index in range(0, 20):
            if index == 10:
                continue
            df['ask_' + str(index) + '_price'] = df['ask_' + str(index) + '_price'].astype(float)
            df['ask_' + str(index) + '_qty'] = df['ask_' + str(index) + '_qty'].astype(float)
            df['bid_' + str(index) + '_price'] = df['bid_' + str(index) + '_price'].astype(float)
            df['bid_' + str(index) + '_qty'] = df['bid_' + str(index) + '_qty'].astype(float)
        return df

    def retreat_all(self):
        df = self.read_from_excel()
        df = self.retreat(df)
        col = ['time']
        for index in range(0, 20):
            if index == 10:
                continue
            col.append('ask_' + str(index) + '_price')
            col.append('ask_' + str(index) + '_qty')
        for index in range(0, 20):
            if index == 10:
                continue
            col.append('bid_' + str(index) + '_price')
            col.append('bid_' + str(index) + '_qty')
        df.to_excel("exporter_outputa.xlsx", columns=col)

class OrderBookGraphDrawer:
    """
    data를 바탕으로 그래프를 그린다.
    """
    _df: pd.DataFrame

    _candledf: pd.DataFrame
    def __init__(self, df: pd.DataFrame, candledf: pd.DataFrame):
        self._df = df
        self._candledf = candledf

    def drawChart(self):
        self._df['ask_qty_0_20'] = 0
        self._df['bid_qty_0_20'] = 0

        for index in range(0, 3):
            if index == 10:
                continue
            self._df['ask_qty_0_20'] += self._df['ask_' + str(index) + '_qty']
        for index in range(0, 3):
            if index == 10:
                continue
            self._df['bid_qty_0_20'] += self._df['bid_' + str(index) + '_qty']
        cols: int = 1
        rows: int = 3
        row_heights = [3, 1, 1]
        subplot_titles = ['메인차트', '애스크양', '비드']
        # for builder in self._indicatorBuilder:
        #     rows += builder.numberOfRows()
        #     row_heights += ([1] * builder.numberOfRows())
        #     subplot_titles += ([builder.name] * builder.numberOfRows())
        fig = make_subplots(rows=rows, cols=cols, shared_xaxes=True,
                            vertical_spacing=0.03, subplot_titles=subplot_titles,
                            row_heights=row_heights)
        self.drawOHLCChart(fig)

        fig.add_trace(
            go.Scatter(x=df['time'], y=df['ask_qty_0_20'],
                       mode='lines',
                       name='애스크 합'),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['bid_qty_0_20'],
                       mode='lines',
                       name='비드 '),
            row=3, col=1
        )
        currentRow: int = 2
        #
        # for builder in self._indicatorBuilder:
        #     figures: [GraphInfo] = builder.draw_graph(self._df)
        #     for figure in figures:
        #         if figure.attachToMainChart:
        #             fig.add_trace(
        #                 figure.graphData,
        #                 row=1, col=1
        #             )
        #         else:
        #             currentRow += 1
        #             fig.add_trace(
        #                 figure.graphData,
        #                 row=currentRow, col=1
        #             )

        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.show()
        fig.write_html("graph/bid_ask.html")

    def drawOHLCChart(self, fig):
        """
        ohlc 차트를 그린다.
        :return:
        """

        # Plot OHLC on 1st row
        fig.add_trace(
            go.Candlestick(x=self._candledf['openTime'], open=self._candledf["open"], high=self._candledf["high"],
                           low=self._candledf["low"], close=self._candledf["close"], name="OHLC"),
            row=1, col=1
        )


if __name__ == '__main__':
    # exporter = OrderBookExporter()
    # exporter.export_all()
    df = pd.read_excel('exporter_output.xlsx')
    crawler = CandleCrawler(symbol='BTCUSDT')
    minTime = df['time'].iloc[0]
    maxTime = df['time'].iloc[-1]
    candle_df = crawler.load_data(crawler.data_save_path, refresh=False, page=5, limit=500, interval=CandlestickInterval.MIN1)
    candle_df = candle_df[(minTime < candle_df['openTime']) & (candle_df['openTime'] < maxTime)]
    # candle_df = pd.read_excel("output_good.xlsx")
    graph = OrderBookGraphDrawer(df, candle_df)
    graph.drawChart()
