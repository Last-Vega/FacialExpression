import csv
import sys
import os
import pandas as pd

df = pd.read_csv('./Batch_4350992_batch_results.csv')
df = df[['HITId', 'WorkerId', 'Answer.category.label']]
df.to_csv('./for_ds.csv', index=False)
