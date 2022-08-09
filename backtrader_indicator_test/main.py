import backtrader as bt
import pandas as pd
import argparse, os, sys
from strategies import macd_test, rsi_test, rsi_signal


# Declare strategies
strategy_dict = {
    "macd_test" : macd_test,
    "rsi_test": rsi_test,
    "rsi_signal": rsi_signal
}

# Init argparse
parser = argparse.ArgumentParser()

# Set argument variable and type
parser.add_argument("strategy", help="Strategy type", type=str)

# Parse arguments 
args = parser.parse_args()

# Check if input is valid

if not args.strategy in strategy_dict.keys():
    print(f"Wrong strategy type. Available strategies: {strategy_dict.keys()}")
    sys.exit()

# Init Cerebro and set broker cash
cerebro = bt.Cerebro()
cerebro.broker.set_cash(1000)

# Load data with pandas and initialize feed
data = pd.read_csv("../../data/BITSTAMP_BTCUSD_DAY.csv", index_col="Date", parse_dates=True)
feed = bt.feeds.PandasData(dataname=data)

# Add data to Cerebro
cerebro.adddata(feed)

# Load chosen strategy
cerebro.addstrategy(strategy_dict[args.strategy])

# Run Cerebro and plot results
cerebro.run()
cerebro.plot()