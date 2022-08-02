import backtrader
import datetime
from strategies import TestStrategy

cerebro = backtrader.Cerebro()

cerebro.broker.set_cash(1000000)


print('Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()


print('Final portfolio Value: %.2f' % cerebro.broker.getvalue())