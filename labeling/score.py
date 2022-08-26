import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

diretorio = 'output/no-manual'
arquivo2 = 'labeled-br-0.05-37625.csv'


colunas = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label', 'label']
df = pd.read_csv(f"{diretorio}/{arquivo2}", encoding='utf-8', sep=',', usecols=colunas)
len(df)

# limpeza e processamento
df = df[df['manual_label'].notna()]  # remove linhas que tenham o campo especifico nulo
df = df[df['landuse_description'].notna()]
df = df.reset_index(drop=True)


y_pred = list(df['label'])
y_true = list(df['manual_label'])
print('Score: ', accuracy_score(y_true, y_pred))
