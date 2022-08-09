import backtrader as bt
from datetime import datetime
from math import floor

# First test of MACD strategy
class macd_test(bt.Strategy):
    params = (
        ("macd_sig", 9),
        ("macd_short", 16),
        ("macd_long", 26),
        ("macd_buy", -0.24),
        ("macd_sell", 0.30),
        ("portfolio_percent", 0.95),
        ("ticker", "BTC")
    )
    
    def log(self, action):
        print("{}: {} {} of {}({}) by {}".format(
            self.data.datetime.date(),
            action,
            self.size,
            self.p.ticker,
            self.data.close[0],
            self.size * self.data.close
        ))

    def calculate_size(self):
        ammount = self.p.portfolio_percent * self.broker.cash
        return ammount / self.data.close

    def __init__(self):
        self.macd = bt.ind.MACD(period_me1=self.p.macd_short, period_me2=self.p.macd_long, period_signal=self.p.macd_sig)
        self.cross_buy = bt.ind.CrossOver(self.macd, self.p.macd_buy)
        self.cross_sell= bt.ind.CrossOver(self.macd, self.p.macd_sell)
    
    def next(self):
        if self.position.size == 0:
            if self.cross_buy == 1.0:
                self.size = self.calculate_size()
                self.log("BUY")
                self.buy(size=self.size)
        else:
            if self.cross_sell == 1.0:
                self.log("SELL")
                self.close()

# First test of an RSI strategy
class rsi_test(bt.Strategy):
    params = (
        ("rsi_per", 14),
        ("sig_top", 70),
        ("sig_bot", 30),
        ("portfolio_percent", 0.1),
        ("ticker", "SPY")
        )
    def calculate_size(self):
        print(self.broker.cash, self.broker.cash * self.p.portfolio_percent, self.broker.cash * self.p.portfolio_percent / self.data.close)
        return self.broker.cash * self.p.portfolio_percent / self.data.close

    def __init__(self):
        
        # Init RSI
        self.rsi = bt.indicators.RSI_SMA(
            self.data,
            period=self.p.rsi_per,
        )
        
        # Define crossovers for using as trading signals
        self.crossup = bt.indicators.CrossOver(self.rsi, self.p.sig_bot),
        self.crossdown = bt.indicators.CrossOver(self.rsi, self.p.sig_top)
        
    def next(self):
        if self.position.size == 0:
            #print(self.crossup[0][0])
            if self.crossup[0][0] == 1.0:
                self.size = self.calculate_size()
                print(f"{self.data.datetime.date()}: BUY {self.size} of {self.params.ticker}({self.data.close[0]}) by {self.data.close[0] * self.size}")
                self.buy(size=self.size)
        else:
            if self.crossdown[0] < 0:
                print(f"{self.data.datetime.date()}: SELL {self.size} of {self.params.ticker}({self.data.close[0]}) by {self.data.close[0] * self.size}")
                self.close()

# RSI oversold/overbought strategy using golden/death cross to
# Determine long-term trend  
class rsi_ma(bt.Strategy):
    pass


# Trying out singal strategies
class rsi_signal(bt.SignalStrategy):
    params = (
        ("rsi_top", 60),
        ("rsi_bot", 20),
        ("rsi_per", 14),
        ("ticker", "SPY"),
        ("portfolio_percent", 0.1)
    )

    def calculate_size(self):
        return self.broker.cash * self.p.portfolio_percent
    
    def __init__(self):
        self.rsi = bt.ind.RSI_SMA(self.data, period=self.p.rsi_per)

        self.crossup = bt.ind.CrossOver(self.rsi, self.p.rsi_bot)
        self.crossdown = bt.ind.CrossOver(self.rsi, self.p.rsi_top)

        self.signal_add(bt.SIGNAL_LONG, self.crossup)
        self.signal_add(bt.SIGNAL_LONGEXIT, self.crossdown)