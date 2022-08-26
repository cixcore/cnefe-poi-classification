import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

diretorio = 'output/no-manual/no-dists'
arquivo2 = 'labeled-br-0.05-37625.csv'

colunas = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label', 'pred_label']
df = pd.read_csv(f"{diretorio}/{arquivo2}", encoding='utf-8', sep=',', usecols=colunas)
len(df)

# limpeza e processamento
df = df[df['manual_label'].notna()]  # remove linhas que tenham o campo especifico nulo
df = df[df['landuse_description'].notna()]
df = df.reset_index(drop=True)

y_pred = list(df['pred_label'])
y_true = list(df['manual_label'])
print('Score: ', accuracy_score(y_true, y_pred))

# gera acertos e totais por classe:
df['igual'] = df.apply(lambda x: 1 if x.manual_label == x.pred_label else 0, axis=1)
df2 = df.groupby('manual_label').agg({'order': 'count', 'igual': 'sum'})
df2 = df2.reset_index(drop=False)
df2.rename(columns={'order': 'total', 'igual': 'corretas'}, inplace=True)
df2['erros'] = df2['total'] - df2['corretas']
with open(f'{diretorio}/lfs-score.txt', 'w') as f:
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(f'{df2}', file=f)

