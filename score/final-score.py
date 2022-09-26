import json
import utils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay

cols = ['order', 'id', 'urban_rural', 'landuse_id', 'landuse_description', 'label', 'lenient_hit', 'anotador1',
        'anotador2', 'hit', 'clf', 'ambiguous', 'match_annotations']
dtype = {'order': int, 'id': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str, 'label': str,
         'lenient_hit': bool, 'anotador1': str, 'anotador2': str, 'hit': bool, 'clf': str,
         'ambiguous': str, 'match_annotations': bool}
df = pd.read_csv('./sample-10-per-class-annotation.csv', encoding='utf-8', sep=',', usecols=cols)
len(df)
df = df[df['id'].notna()]

# add column for lenient evaluation
df['anotador3'] = np.where(df['lenient_hit'], df.label, df.anotador1)
df['landuse_description'] = df['landuse_description'].map(utils.description)
print(df)

# value_tuples = list(df[['landuse_id', 'landuse_description']].apply(tuple, axis=1))
# print(value_tuples)

for classifier in ['svc', 'rf', 'lr', 'snorkel', 'bert']: #'svc', 'rf', 'lr', 'bert',
    print(f'\nProcessing {classifier}...')
    output_dir = f'./{classifier}'
    if classifier == 'snorkel':
        predictions = pd.read_csv('../labeling/output/br/snorkel-just-phonetic/labeled.csv', encoding='utf-8',
                                  dtype={'landuse_description': str, 'label': str, 'landuse_id': int},
                                  usecols=['landuse_description', 'label', 'landuse_id'])
        predictions['landuse_description'] = predictions['landuse_description'].map(utils.description)
    else:
        predictions = pd.read_csv(f'../learning/{classifier}-training/labeled-br.csv', encoding='utf-8',
                                  dtype={'landuse_description': str, 'label': str, 'landuse_id': int},
                                  usecols=['landuse_description', 'label', 'landuse_id'])

    descriptions = predictions['landuse_description'].apply(lambda x: len(x.split()))
    print(f'{predictions["landuse_description"][0:10]}')
    print(f'{descriptions[0:10]}')
    max_words = max(descriptions)
    for item in predictions["landuse_description"]:
        if len(item.split()) == max_words:
            print(item)
    print(f'max(descriptions): {max_words}')
    print(f'len(descriptions): {len(descriptions)}')
    print(f'sum(descriptions): {sum(descriptions)}')
    print(f'sum/len(descriptions): {sum(descriptions)/len(descriptions)}')

    ids = []
    ambiguous = []
    landuse_description = []
    landuse_id = []
    y_pred = []
    y_true = []
    y_true_lenient = []
    for index, row in df.iterrows():
        series = predictions.loc[(predictions['landuse_id'] == row.landuse_id)
                                 & (predictions['landuse_description'] == row.landuse_description)].iloc[0]
        y_pred.append(str(series.label))
        y_true.append(str(row.anotador1))
        y_true_lenient.append(str(row.anotador3))
        landuse_description.append(str(row.landuse_description))
        landuse_id.append(int(row.landuse_id))
        ids.append(int(row.id))
        if pd.isnull(row.ambiguous):
            ambiguous.append('N')
        else:
            ambiguous.append(str(row.ambiguous))
        if index % 90 == 0:
            print(index)

    df1 = pd.DataFrame({
        'id': ids,
        'landuse_id': landuse_id,
        'landuse_description': landuse_description,
        'label': y_pred,
        'anotador1': y_true,
        'ambiguous': ambiguous,
        'anotador3': y_true_lenient
    })
    # print(df1)
    df1.to_csv(f'{output_dir}.csv', index=False, encoding='utf-8')

    fig, ax = plt.subplots(figsize=(14, 14))
    plt.rcParams.update({'font.size': 8})
    cm = confusion_matrix(y_true=y_true, y_pred=y_pred, labels=utils.labels_list())
    ConfusionMatrixDisplay(cm).plot(ax=ax, cmap=plt.cm.YlGnBu)
    plt.savefig(f'{output_dir}-confusion-matrix.pdf', bbox_inches='tight', pad_inches=0)

    fig, ax = plt.subplots(figsize=(14, 14))
    plt.rcParams.update({'font.size': 8})
    cm = confusion_matrix(y_true=y_true_lenient, y_pred=y_pred, labels=utils.labels_list())
    ConfusionMatrixDisplay(cm).plot(ax=ax, cmap=plt.cm.YlGnBu)
    plt.savefig(f'{output_dir}-confusion-matrix-lenient.pdf', bbox_inches='tight', pad_inches=0)
    """
    # Save score
    with open(f'{output_dir}-scores.json', 'w') as f:
        scores = {
            'accuracy': accuracy_score(y_true, y_pred),
            'f1_macro': f1_score(y_true, y_pred, average='macro'),
            'f1_micro': f1_score(y_true, y_pred, average='micro'),
            'accuracy_lenient': accuracy_score(y_true_lenient, y_pred),
            'f1_macro_lenient': f1_score(y_true_lenient, y_pred, average='macro'),
            'f1_micro_lenient': f1_score(y_true_lenient, y_pred, average='micro')
        }
        json.dump(scores, f)

    df1['equal'] = df1.apply(lambda x: 1 if str(x.label) == str(x.anotador1) else 0, axis=1)
    df1['ambiguity_count'] = df1.apply(lambda x: 1 if x.ambiguous == 'S' else 0, axis=1)
    df2 = df1.groupby('anotador1').agg({'id': 'count', 'equal': 'sum', 'ambiguity_count': 'sum'})
    df2 = df2.reset_index(drop=False)
    df2.rename(columns={'id': 'total', 'equal': 'hits'}, inplace=True)
    df2['errors'] = df2['total'] - df2['hits']
    df2['errors%'] = df2['errors'] / df2['total']
    df2.to_csv(f'{output_dir}-score-per-class.csv', index=False, encoding='utf-8')

    # Save lenient score
    df1['equal'] = df1.apply(lambda x: 1 if str(x.label) == str(x.anotador3) else 0, axis=1)
    df1['ambiguity_count'] = df1.apply(lambda x: 1 if x.ambiguous == 'S' else 0, axis=1)
    df2 = df1.groupby('anotador3').agg({'id': 'count', 'equal': 'sum', 'ambiguity_count': 'sum'})
    df2 = df2.reset_index(drop=False)
    df2.rename(columns={'id': 'total', 'equal': 'hits'}, inplace=True)
    df2['errors'] = df2['total'] - df2['hits']
    df2['errors%'] = df2['errors'] / df2['total']
    df2.to_csv(f'{output_dir}-score-per-class_lenient.csv', index=False, encoding='utf-8')
    """
