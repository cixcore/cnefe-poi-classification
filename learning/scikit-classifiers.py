import nltk
import json
import utils
import numpy as np
import pandas as pd
import seaborn as sns
from time import time
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
from sklearn.metrics import accuracy_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_validate, cross_val_predict, GridSearchCV


def import_csv(filepath, has_manual):
    cols = ['urban_rural', 'landuse_id', 'landuse_description']
    dtype = {'urban_rural': int, 'landuse_id': int, 'landuse_description': str}
    if has_manual:
        cols.append('manual_label')
        dtype['manual_label'] = str
    # clean data
    df = pd.read_csv(filepath, encoding='utf-8', dtype=dtype, usecols=cols)
    df = df[df['landuse_description'].notna()]
    df['landuse_description'] = df['landuse_description'].str \
        .normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df.drop(df[df['landuse_description'].str.isnumeric()].index, axis=0, inplace=True)
    df['landuse_description'] = df['landuse_description'].map(utils.description)
    if has_manual:
        df = df[df['manual_label'].notna()]
    df = df.reset_index(drop=True)
    print('Count:', len(df))

    count_token_insight = False
    if count_token_insight:
        print("Generating count token pdf...")
        df['count_tokens'] = df.apply(lambda x: len(nltk.word_tokenize(x['landuse_description'])), axis=1)
        plot_count_tokens = df.groupby('count_tokens').count()
        print(plot_count_tokens)
        sns.barplot(x=plot_count_tokens.index, y=plot_count_tokens.landuse_description, data=plot_count_tokens)
        plt.savefig('token_count.pdf')

    if has_manual:
        print("Generating label count csv...")
        dfc = df.groupby('manual_label').count()
        dfc.to_csv(f'./manual-annotation-distribution.csv', encoding='utf-8', index=False)
    return df


nltk.download('punkt')

directory = '.'
file = 'manual-annotation-0.05-37625.csv'
print(f'\n# Open and clean up {file}...')
df_manual = import_csv(f'{directory}/{file}', has_manual=True)

# string classes to int
utils.label_str_to_int(df_manual)
df_manual.reset_index(drop=True, inplace=True)
df_manual = df_manual.drop_duplicates(['landuse_id', 'landuse_description', 'manual_label'])
print(len(df_manual))

df2 = df_manual.groupby('label').count()
sns.barplot(x=df2.index, y=df2.manual_label, data=df2)
plt.savefig('label_dist.pdf')

should_generate_train = False
if should_generate_train:
    time_to_vectorize = time()
    print('Vectorizing manual-labeled.csv with tf-idf...')
    transformer = ColumnTransformer(
        transformers=[
            ('description', TfidfVectorizer(), 'landuse_description'),
            ('id', OneHotEncoder(), ['landuse_id'])
        ]
    )
    X_train = transformer.fit_transform(df_manual[['landuse_id', 'landuse_description']])
    print(f'Finished vectorizing. (took {time() - time_to_vectorize}s)')

    y_true = np.array(df_manual['label'].astype(int))
    print(f'Saving X_train, y_true...')
    dump(X_train, './X_train.joblib')
    dump(y_true, './y_true.joblib')
    dump(transformer, './transformer.joblib')
else:
    print(f'Loading X_train, y_true...')
    X_train = load('./X_train.joblib')
    y_true = load('./y_true.joblib')
    transformer = load('./transformer.joblib')

print(X_train.shape)
print(len(y_true))

seed = 1
choose = 3
if choose == 3:
    clf = RandomForestClassifier(random_state=seed)
    param_grid = {'n_estimators': [100]}
    output_dir = 'rf-training'
    print('\nRunning random forest...')
elif choose == 2:
    clf = svm.SVC(random_state=seed)
    param_grid = {"C": [1.0]}
    output_dir = 'svc-training'
    print('\nRunning SVM...')
else:
    clf = LogisticRegression(random_state=seed)
    param_grid = {"C": [1.0]}
    output_dir = 'lr-training'
    print('\nRunning logistic regression...')

metric = ['accuracy', 'f1_macro', 'f1_micro']

cv = 1
gridsr = 2
choice = 1
if choice == cv:
    print('# Cross Validation predict...')
    time_cv = time()
    # scores = cross_validate(clf, X_train, y_true, cv=None, scoring=metric, n_jobs=-1)
    y_preds = cross_val_predict(clf, X_train, y_true, cv=None, n_jobs=-1)
    print(f'Finished CV. (took {(time() - time_cv):.2f}s)')

    print('\n# Saving CV scores..')
    with open(f'{output_dir}/scores.json', 'w') as f:
        scores = {
            'accuracy': {
                # 'mean': mean(scores['test_accuracy']),
                # 'std': std(scores['test_accuracy']),
                'predicts': accuracy_score(y_true, y_preds)
            },
            'f1_macro': {
                # 'mean': mean(scores['test_f1_macro']),
                # 'std': std(scores['test_f1_macro']),
                'predicts': f1_score(y_true, y_preds, average='macro')
            },
            'f1_micro': {
                # 'mean': mean(scores['test_f1_micro']),
                # 'std': std(scores['test_f1_micro']),
                'predicts': f1_score(y_true, y_preds, average='micro')
            }
        }
        json.dump(scores, f)
else:  # choice == gridsr
    estimator = clf
    clf = GridSearchCV(estimator=estimator, param_grid=param_grid, verbose=3, n_jobs=-1,
                       scoring=('accuracy', 'f1_macro', 'f1_micro'), refit='f1_macro')

print('# Fitting whole training set...')
time_learning = time()
clf.fit(X_train, y_true)
print(f'Finished learning. (took {(time() - time_learning):.2f}s)')
dump(clf, f'{output_dir}/clf.joblib')
# clf = load(f'{output_dir}/clf.joblib')

print('\n# Predict br.csv...')
time_to_import_csv = time()
print('# Open and clean up ../sampling/BR.csv.csv...')
df_br = import_csv('../sampling/BR.csv', has_manual=False)
print(f'Finished importing csv. (took {time() - time_to_import_csv}s)')

time_predicting = time()
time_to_transform = time()
print('Vectorizing br.csv with tf-idf...')
X_all = transformer.transform(df_br[['landuse_id', 'landuse_description']])
print(f'Finished transforming br data. (took {time() - time_to_transform}s)')

y_pred = clf.predict(X_all)
print(f'Finished predicting. (took {(time() - time_predicting):.2f}s)')

df_br.index.name = 'id'
print('# Save to .csv')
df_br.assign(label=[utils.get_label_name(p) for p in y_pred], pred_label=y_pred) \
    .to_csv(f'{output_dir}/labeled-br.csv', encoding='utf-8')
# clf = load(f'{output_dir}/clf.joblib')

print('\nDone :).')
