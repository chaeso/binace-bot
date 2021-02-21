import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from candlecrawler import *


class GraphDrawer:
    """
    data를 바탕으로 그래프를 그린다.
    """
    _df: pd.DataFrame

    _indicatorBuilder: [BaseIndicatorBuilder]

    def __init__(self, df: pd.DataFrame, indicatorBuilder: [BaseIndicatorBuilder]):
        self._df = df
        self._indicatorBuilder = indicatorBuilder

    def drawChart(self):

        cols: int = 1
        rows: int = 2
        row_heights = [2, 1]
        subplot_titles = ['OHLC', 'Volume']
        for builder in self._indicatorBuilder:
            rows += builder.numberOfRows()
            row_heights += ([1] * builder.numberOfRows())
            subplot_titles += ([builder.name] * builder.numberOfRows())
        fig = make_subplots(rows=rows, cols=cols, shared_xaxes=True,
                            vertical_spacing=0.03, subplot_titles=subplot_titles,
                            row_heights=row_heights)
        self.drawOHLCChart(fig)

        currentRow: int = 2

        for builder in self._indicatorBuilder:
            figures: [GraphInfo] = builder.draw_graph(self._df)
            for figure in figures:
                if figure.attachToMainChart:
                    fig.add_trace(
                        figure.graphData,
                        row=1, col=1
                    )
                else:
                    currentRow += 1
                    fig.add_trace(
                        figure.graphData,
                        row=currentRow, col=1
                    )

        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.show()

    def drawOHLCChart(self, fig):
        """
        ohlc 차트를 그린다.
        :return:
        """
        # Plot OHLC on 1st row
        fig.add_trace(
            go.Candlestick(x=self._df['openTime'], open=self._df["open"], high=self._df["high"],
                           low=self._df["low"], close=self._df["close"], name="OHLC"),
            row=1, col=1
        )

        # Bar trace for volumes on 2nd row without legend
        fig.add_trace(go.Bar(x=self._df['openTime'], y=self._df['volume'], showlegend=False), row=2, col=1)



if __name__ == '__main__':
    crawler = CandleCrawler(symbol="BTCUSDT")
    df = crawler.load_data(crawler.data_save_path, refresh=True, page=1, limit=500, interval=CandlestickInterval.MIN1)

    graphDrawer = GraphDrawer(df, crawler.indiecatorBuilder)
    graphDrawer.drawChart()