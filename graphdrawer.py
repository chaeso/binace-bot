import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from candlecrawler import *


class GraphDrawer:
    """
    data를 바탕으로 그래프를 그린다.
    """
    _df: pd.DataFrame

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def drawOHLCChart(self):
        """
        ohlc 차트를 그린다.
        :return:
        """
        # Create subplots and mention plot grid size
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'),
                            row_width=[0.2, 0.7])

        # Plot OHLC on 1st row
        fig.add_trace(
            go.Candlestick(x=df['openTime'], open=df["open"], high=df["high"],
                           low=df["low"], close=df["close"], name="OHLC"),
            row=1, col=1
        )

        # Bar trace for volumes on 2nd row without legend
        fig.add_trace(go.Bar(x=df['openTime'], y=df['volume'], showlegend=False), row=2, col=1)

        # Do not show OHLC's rangeslider plot
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.show()


if __name__ == '__main__':
    crawler = CandleCrawler()
    df = crawler.load_data(crawler.data_save_path, refresh=True, page=1, limit=500, interval=CandlestickInterval.MIN1)

    print(df)
    graphDrawer = GraphDrawer(df)
    graphDrawer.drawOHLCChart()