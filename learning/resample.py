import utils
import pandas as pd
from time import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--do_snorkel_append', action='store_const', const=True,
                        help='import and append snorkel classification to csv')
    parser.add_argument('-c', '--do_clfs_append', action='store_const', const=True,
                        help='import and append rf, svm and lr classification to csv')
    parser.add_argument('-b', '--do_bert_append', action='store_const', const=True,
                        help='import and append bert classification to csv')
    parser.add_argument('-p', '--do_previous_append', action='store_const', const=True,
                        help='import and append already generated resample to csv')
    return parser.parse_args()


if __name__ == '__main__':
    output_file = 'new-sample-classified-br.csv'
    args = parse_args()
    classifiers = ['rf', 'svc', 'lr']
    snorkel_output = '../labeling/output/br/snorkel-just-phonetic/labeled.csv'
    cols = ['id', 'urban_rural', 'landuse_id', 'landuse_description', 'label']
    dtype = {'id': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str, 'label': str}

    time_to_import_csv = time()
    manual_df = pd.read_csv('./sample-br-0.05-37625-manual-labeled.csv', encoding='utf-8',
                            dtype={'urban_rural': int, 'landuse_id': int, 'landuse_description': str,
                                   'manual_label': str},
                            usecols=['urban_rural', 'landuse_id', 'landuse_description', 'manual_label'])
    manual_df = manual_df[manual_df['manual_label'].notna()]
    print(f'Finished importing and cleaning manual labeled instances csv. (took {time() - time_to_import_csv}s)')

    if not args.do_previous_append:
        df = pd.DataFrame()
    else:
        print(f'Starting from previous {output_file}...')
        df = pd.read_csv(f'./{output_file}', encoding='utf-8',
                         dtype={'order': int, 'id': int, 'urban_rural': int, 'landuse_id': int,
                                'landuse_description': str, 'label': str, 'clf': str},
                         usecols=['order', 'id', 'urban_rural', 'landuse_id', 'landuse_description', 'label', 'clf'])

    if args.do_snorkel_append:
        time_to_import_csv = time()
        snorkel_df = pd.read_csv(snorkel_output, encoding='utf-8', dtype=dtype, usecols=cols)
        snorkel_df['clf'] = 'snorkel'
        print(f'Finished importing snorkel labeled instances csv. (took {time() - time_to_import_csv}s)')
        labels = list(snorkel_df['label'].unique())
        for label in labels:
            df1 = snorkel_df[snorkel_df.label == label]
            df1 = df1[~df1.landuse_description.isin(manual_df.landuse_description)]
            if len(df1) > 80:
                df2 = df1.sample(80, random_state=1)
            else:
                df2 = df1
            df2['landuse_description'] = df2['landuse_description'].drop_duplicates()
            df2 = df2[df2['landuse_description'].notna()]
            df = pd.concat([df, df2.sample(10, random_state=1)])

    if args.do_clfs_append:
        for clf in classifiers:
            print(f'\nImporting {clf.upper()} labeled instances...')
            time_to_import_csv = time()
            clf_df = pd.read_csv(f'./{clf}-training/labeled-br.csv', encoding='utf-8', dtype=dtype, usecols=cols)
            print(len(clf_df))
            print(f'Finished importing {clf.upper()} labeled instances csv. (took {time() - time_to_import_csv}s)')

            clf_df['clf'] = clf
            labels = list(clf_df['label'].unique())

            for label in labels:
                df1 = clf_df[clf_df.label == label]
                df1 = df1[~df1.landuse_description.isin(manual_df.landuse_description)]
                if len(df1) > 80:
                    df2 = df1.sample(80, random_state=1)
                else:
                    df2 = df1
                df2['landuse_description'] = df2['landuse_description'].drop_duplicates()
                df2 = df2[df2['landuse_description'].notna()]
                if len(df2) < 10:
                    sample = df2.sample(frac=1)
                else:
                    sample = df2.sample(10)
                df = pd.concat([df, sample])

    if args.do_bert_append:
        time_to_import_csv = time()
        bert_df = pd.read_csv('./bert-training/labeled-br.csv', encoding='utf-8', dtype=dtype, usecols=cols)
        bert_df['clf'] = 'bert'
        print(f'Finished importing bert labeled instances csv. (took {time() - time_to_import_csv}s)')
        labels = list(bert_df['label'].unique())
        for label in labels:
            df1 = bert_df[bert_df.label == label]
            df1 = df1[~df1.landuse_description.isin(manual_df.landuse_description)]
            if len(df1) > 80:
                df2 = df1.sample(80, random_state=1)
            else:
                df2 = df1
            df2['landuse_description'] = df2['landuse_description'].drop_duplicates()
            df2 = df2[df2['landuse_description'].notna()]
            if len(df2) < 10:
                sample = df2.sample(frac=1)
            else:
                sample = df2.sample(10)
            df = pd.concat([df, sample])

    print('Saving sample csv...')
    df.reset_index(drop=True, inplace=True)
    df.index.name = 'order'
    df.to_csv(f'./{output_file}-bert', encoding='utf-8')

    print('Done :).')
