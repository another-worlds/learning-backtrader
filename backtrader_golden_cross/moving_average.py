import backtrader as bd
from datetime import datetime

closing_price_sum = 0

with open("data/SPY.csv") as f:
    for line in f.readlines()[-50:]:
        tokens = line.split(',')
        print(tokens[4])
        closing_price = float(tokens[4])

        closing_price_sum += closing_price
    
print(closing_price_sum / 50)