import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../../data/BITSTAMP_BTCUSD_HOUR.csv", parse_dates=True)
print(df.head())