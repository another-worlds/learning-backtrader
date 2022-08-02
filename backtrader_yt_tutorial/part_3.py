import backtrader
import datetime
from strategies import TestStrategy_v3

cerebro = backtrader.Cerebro()

cerebro.broker.set_cash(100)

# Load Data
data = backtrader.feeds.YahooFinanceCSVData(
    dataname='data/oracle.csv',
    fromdate=datetime.datetime(1995, 1, 3),
    todate=datetime.datetime(2014, 12, 31),
    reverse=False
)

# Add data to tester
cerebro.adddata(data)

# Add strategy to tester
cerebro.addstrategy(TestStrategy_v3)

cerebro.addsizer(backtrader.sizers.FixedSize, stake=10)

print('Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run tester
cerebro.run()

print('Final portfolio Value: %.2f' % cerebro.broker.getvalue())