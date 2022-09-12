import nltk
import utils
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import svm
from numpy import mean, std
from joblib import dump, load
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from sklearn import metrics
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_validate, KFold, GridSearchCV


nltk.download('punkt')
directory = '.'
file = 'sample-br-0.05-37625-manual-labeled.csv'

cols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label']  # , 'pred_label']
df = pd.read_csv(f"{directory}/{file}", encoding='utf-8', sep=',', usecols=cols)

df['landuse_description'] = df['landuse_description'].str.lower()
df = df[df['landuse_description'].notna()]
df = df[df['manual_label'].notna()]
df['landuse_description'] = df['landuse_description'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df.drop(df[df['landuse_description'].str.isnumeric()].index, axis=0, inplace=True)

df = df.reset_index(drop=True)
print('Labeled count:', len(df))

df['landuse_description'] = df['landuse_description'].map(utils.description)


df['count_tokens'] = df.apply(lambda x: len(nltk.word_tokenize(x['landuse_description'])), axis=1)
df2 = df.groupby('count_tokens').count()
sns.barplot(x=df2.index, y=df2.order, data=df2)
plt.savefig('token_count.pdf')


print(df[df['landuse_description'].str.find('const') > -1]['landuse_description'])

# string classes to int
utils.label_str_to_int(df)
df.reset_index(drop=True, inplace=True)

df2 = df.groupby('label').count()
sns.barplot(x=df2.index, y=df2.manual_label, data=df2)
plt.savefig('label_dist.pdf')

# tf-idf
transformer = ColumnTransformer(
    transformers=[
        ('description', TfidfVectorizer(), 'landuse_description'),
        ('id', OneHotEncoder(), ['landuse_id'])
    ]
)
X = transformer.fit_transform(df[['landuse_id', 'landuse_description']])
y = np.array(df['label'].astype(int))


seed = 1
# print(sorted(metrics.SCORERS.keys()))
choose = 1
if choose == 1:
    clf = RandomForestClassifier(n_estimators=100, random_state=seed)
    output_dir = 'rf-training'
elif choose == 2:
    clf = svm.SVC(kernel='linear', C=1, random_state=seed)
    output_dir = 'svc-training'
else:
    clf = LogisticRegression(random_state=seed)
    output_dir = 'lr-training'

metric = ['accuracy', 'f1_macro', 'f1_micro']

# Cross Validation: simples
scores = cross_validate(clf, X, y, cv=10, scoring=metric, n_jobs=-1)
print(scores)
dump(clf, f'{output_dir}/clf.joblib')

# clf = load(f'{output_dir}/clf.joblib')

