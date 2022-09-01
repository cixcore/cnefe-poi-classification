import re
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import svm
from numpy import mean, std
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
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
dir = '../labeling/output/no-manual/just-phonetic'
file = 'labeled-br-0.05-37625.csv'

cols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label', 'pred_label']
df = pd.read_csv(f"{dir}/{file}", encoding='utf-8', sep=',', usecols=cols)

# ajusta textos
df['landuse_description'] = df['landuse_description'].str.lower()
df = df[df['landuse_description'].notna()]
df['landuse_description'] = df['landuse_description'].str \
    .normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df.drop(df[df['landuse_description'].str.isnumeric()].index, axis=0, inplace=True)
df = df[df['manual_label'].notna()]  # remove linhas que tenham o campo especifico nulo
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

# calcula   embeddings esparsas tf-idf
docs = list(df['landuse_description'])
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)
y = np.array(df['label'].astype(int))

# X: (linhas: instancias, colunas:palavras)
X.shape, y.shape, len(vectorizer.vocabulary_)

# Verifica documento 10
d = 10
print(docs[d])
# verifica scores da palavras do documento 10
a = X[d].toarray()
idx = np.where(a[0] > 0)

# Cross Validation: simples
seed = 1
# clf = svm.SVC(kernel='linear', C=1, random_state=1)
clf = RandomForestClassifier(n_estimators=100, random_state=seed)
metrica = 'accuracy'  # f1_macro
scores = cross_val_score(clf, X, y, cv=10, scoring=metrica, )

print(f'{metrica}: %.3f (%.3f)' % (mean(scores), std(scores)))

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
search = GridSearchCV(model, space, scoring=metrica, n_jobs=1, cv=cv_inner, refit=True)

# configure the cross-validation procedure
cv_outer = KFold(n_splits=10, shuffle=True, random_state=1)
# execute the nested cross-validation
scores = cross_val_score(search, X, y, scoring=metrica, cv=cv_outer, n_jobs=-1)
# report performance
print(f'{metrica}: %.3f (%.3f)' % (mean(scores), std(scores)))
