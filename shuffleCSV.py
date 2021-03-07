import csv
import random
import pandas as pd

df = pd.read_csv('./amt.csv')
df_shuffled=df.sample(frac=1).reset_index(drop=True)
df_shuffled.to_csv('./shuffled_amt.csv', index=False)
