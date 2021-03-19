import pandas as pd
import matplotlib as plt

df = pd.read_csv('Batch_4350992_batch_results.csv')
dict = {}
workers = df['WorkerId']

for worker in df['WorkerId']:
    if worker not in dict.keys():
        dict[worker] = 1
    else:
        dict[worker] += 1

print(dict)

print(sum(dict.values()))
