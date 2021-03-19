import pandas as pd
import matplotlib as plt

def calc_workers_enthusiasm(f):
    df = pd.read_csv(f)
    dict = {}
    workers = df['WorkerId']

    for worker in df['WorkerId']:
        if worker not in dict.keys():
            dict[worker] = 1
        else:
            dict[worker] += 1

    print(f, 'workers', dict)

    # print(sum(dict.values()))

calc_workers_enthusiasm('./Batch_4350992_batch_results.csv')
calc_workers_enthusiasm('./Batch_4369243_batch_results.csv')
