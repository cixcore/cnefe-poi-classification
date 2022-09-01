import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

directory = 'labeling/output/no-manual/just-phonetic'
file = 'labeled-br-0.05-37625.csv'

cols = ['id', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label', 'pred_label']
df = pd.read_csv(f"{directory}/{file}", encoding='utf-8', sep=',', usecols=cols)
len(df)

df = df[df['manual_label'].notna()]
df = df[df['landuse_description'].notna()]
df = df.reset_index(drop=True)

y_pred = list(df['pred_label'])
y_true = list(df['manual_label'])
print('Score: ', accuracy_score(y_true, y_pred))
print('macro f1: ', f1_score(y_true, y_pred, average='macro'))
print('micro f1: ', f1_score(y_true, y_pred, average='micro'))

df['equal'] = df.apply(lambda x: 1 if x.manual_label == x.pred_label else 0, axis=1)
df2 = df.groupby('manual_label').agg({'id': 'count', 'equal': 'sum'})
df2 = df2.reset_index(drop=False)
df2.rename(columns={'id': 'total', 'equal': 'hits'}, inplace=True)
df2['errors'] = df2['total'] - df2['hits']
df2['errors%'] = df2['errors'] / df2['total']
df2.to_csv(f'{directory}/lfs-score.csv', index=False, encoding='utf-8')

