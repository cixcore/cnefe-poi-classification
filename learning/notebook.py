import re
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import svm
from numpy import mean, std
import matplotlib.pyplot as plt
from transformers import BertTokenizer
from nltk.tokenize import word_tokenize
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score, KFold, GridSearchCV


def description(landuse_description):
    return re.sub(r'[^a-zA-Z0-9\s]', '',
                  re.sub(r'[áãâà]', 'a',
                         re.sub(r'[éẽê3]', 'e',
                                re.sub(r'[íĩî1]', 'i',
                                       re.sub(r'[óõô0]', 'o',
                                              re.sub(r'[úũûü]', 'u',
                                                     re.sub(r'[ç]', 'c', str(landuse_description))))))))


nltk.download('punkt')
directory = '.'
file = 'sample-br-0.05-37625-manual-labeled.csv'

cols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label']  # , 'pred_label']
df = pd.read_csv(f"{directory}/{file}", encoding='utf-8', sep=',', usecols=cols)

# ajusta textos
df['landuse_description'] = df['landuse_description'].str.lower()
df = df[df['landuse_description'].notna()]
df['landuse_description'] = df['landuse_description'].str \
    .normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df.drop(df[df['landuse_description'].str.isnumeric()].index, axis=0, inplace=True)
df = df[df['manual_label'].notna()]
df = df.reset_index(drop=True)
print('Base rotulada:', len(df))

df['landuse_description'] = df['landuse_description'].map(description)

# verifica tokens
df['count_tokens'] = df.apply(lambda x: len(nltk.word_tokenize(x['landuse_description'])), axis=1)
df2 = df.groupby('count_tokens').count()
sns.barplot(x=df2.index, y=df2.order, data=df2)
plt.show()

# verifica palavras
ocorrencia = 'const'  # 'em const'
df[df['landuse_description'].str.find(ocorrencia) > -1]['landuse_description']

# cria classes numericas
df['label'] = ''
classes = df['manual_label'].unique()
for i in range(len(classes)):
    c = classes[i]
    df.loc[df[df['manual_label'] == c].index, 'label'] = i
classes = list(df['manual_label'].unique())
df2 = df.groupby('label').count()
sns.barplot(x=df2.index, y=df2.manual_label, data=df2)
plt.show()

# calcula embeddings esparsas tf-idf
transformer = ColumnTransformer(
    transformers=[
        ('description', TfidfVectorizer(), 'landuse_description'),
        ('id', OneHotEncoder(), ['landuse_id'])
    ]
)
X = transformer.fit_transform(df[['landuse_id', 'landuse_description']])
y = np.array(df['label'].astype(int))

# X: (linhas: instancias, colunas:palavras) X.shape, y.shape, len(vectorizer.vocabulary_)

d = 10
# Verifica documento 10
# print(docs[d])
# verifica scores da palavras do documento 10
a = X[d].toarray()
idx = np.where(a[0] > 0)

# Cross Validation: simples
seed = 1

choose = 1
if choose == 1:
    clf = RandomForestClassifier(n_estimators=100, random_state=seed)
elif choose == 2:
    clf = svm.SVC(kernel='linear', C=1, random_state=seed)
elif choose == 3:
    clf = LogisticRegression(random_state=seed)
elif choose == 4:
    tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', do_lower_case=False)
    clf = tokenizer
elif choose == 4:
    tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', do_lower_case=False)
    clf = tokenizer

metric = 'accuracy'  # f1_macro
scores = cross_val_score(clf, X, y, cv=10, scoring=metric, )

print(f'{metric}: %.3f (%.3f)' % (mean(scores), std(scores)))

# Nested cross validation e gridsearch:
# para otimizar hiperparametros usar isso para evitar ofertiting
# https://machinelearningmastery.com/nested-cross-validation-for-machine-learning-with-python/

# configure the cross-validation procedure
cv_inner = KFold(n_splits=10, shuffle=True, random_state=seed)
# define the model
model = RandomForestClassifier(random_state=seed)
# define search space
space = dict()
space['n_estimators'] = [10, 100]
# space['max_features'] = [2, 4, 6]
# define search
search = GridSearchCV(model, space, scoring=metric, n_jobs=1, cv=cv_inner, refit=True)

# configure the cross-validation procedure
cv_outer = KFold(n_splits=10, shuffle=True, random_state=1)
# execute the nested cross-validation
scores = cross_val_score(search, X, y, scoring=metric, cv=cv_outer, n_jobs=-1)
# report performance
print(f'{metric}: %.3f (%.3f)' % (mean(scores), std(scores)))
