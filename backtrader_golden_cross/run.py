# Import required modules
import os, sys, argparse
import pandas as pd
import backtrader as bt
from strategies import GoldenCross, BuyAndHold

# Init strategy names
strategy_dict = {
    "goldencross": GoldenCross,
    "buyandhold": BuyAndHold
}

# 1. Init and set argparser
parser = argparse.ArgumentParser()
parser.add_argument('strategy', help="Which strategy to use", type=str)

# 2. Get arguments
args = parser.parse_args()
if not args.strategy in strategy_dict:
    print(f"Invalid strategy.\n Choose a strategy from: {strategy_dict.keys()}")
    sys.exit()

# 3. Init Cerebro and set cash
cerebro = bt.Cerebro()
cerebro.broker.set_cash(1000)

# 4. Load data and pass it to cerebro
spy_prices = pd.read_csv("data/SPY.csv", index_col='Date', parse_dates=True)
feed = bt.feeds.PandasData(dataname=spy_prices)
cerebro.adddata(feed)

# 5. Load strategy and set 
cerebro.addstrategy(strategy_dict[args.strategy])

# 6. Run cerebro and plot results
cerebro.run()
cerebro.plot()