import backtrader as bt
from math import floor


class GoldenCross(bt.Strategy):
    # Define parameters of the strategy
    params = (("fast", 50), ("slow", 200), ("portfolio_percentage", 0.95), ("ticker", "SPY"))

    def __init__(self):
  
        # Init fast sma (50)
        self.sma_fast = bt.indicators.SMA(
            self.data.close, period=self.params.fast, plotname="50-day MA"
        )
        # Init slow sma (200)
        self.sma_slow = bt.indicators.SMA(
            self.data.close, period=self.params.slow, plotname="200-day MA"
        )
        # Init crossover indicator
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)
    
    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                print(self.crossover > 0)
                buy_ammount = (self.params.portfolio_percentage * self.broker.cash)
                self.size = floor(buy_ammount / self.data.close)
                self.buy(size=self.size)
    
                print(f"{self.data.datetime.date()}: BUY {self.size} of {self.params.ticker} by {self.data.close[0]}")

        if self.position.size > 1:
            if self.crossover < 0:
                self.close()
                print(f"{self.data.datetime.date()}: SELL {self.size} of {self.params.ticker} by {self.data.close[0]}")

class BuyAndHold(bt.Strategy):
    def next(self):
        self.size = (self.broker.cash / self.data.close)
        self.buy(size=self.size)
