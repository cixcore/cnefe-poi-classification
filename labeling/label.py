import pandas as pd
from snorkel.labeling import PandasLFApplier, LFAnalysis
from snorkel.labeling.model import LabelModel, MajorityLabelVoter
from snorkel.analysis import get_label_buckets
from word_dists import dists
import cnae_scheme
import argparse
import lf


def parse_args():
    parser = argparse.ArgumentParser()

    # 'shuffle-sample-BR-0.05-37625.csv', 'sample-br-0.05-37625-semduplic-reduced'
    filename_open = 'sample-br-0.05-37625-semdup-manual-fix'
    filename_close = f'labeled-{filename_open}'

    parser.add_argument('-w', '--write_lfs', action='store_const', const=True, default=False,
                        help='write labeling funcs output to file')
    parser.add_argument('-e', '--edition_dist', action='store_const', const=True, default=False,
                        help='use levenshtein distance with qwerty wights functions')
    parser.add_argument('-p', '--phonetic_dist', action='store_const', const=True, default=False,
                        help='use portuguese soundex distance functions')
    parser.add_argument('-d', '--data_path', type=str, default=f'./input/{filename_open}.csv', help='path to csv')
    parser.add_argument('-o', '--output_path', type=str, default=f'./output/{filename_close}.csv',
                        help='file to save labeling')
    parser.add_argument('-l', '--label_method', type=str, default='f',
                        help='label method to apply, can be <f>irst match, <s>norkel model, <m>ajority')
    parser.add_argument('-s', '--seed', type=int, default=37625,
                        help='defines seed to be used in sample.random_state to reproduce results')
    return parser.parse_args()


def import_csv(filepath):
    print(f'\nReading from file "{filepath}"...')
    cols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label']
    dtype = {'order': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str, 'manual_label': str}
    # cols = ['ordem', 'urban_rural', 'landuse_id', 'landuse_description', 'categoria_cnae']
    # dtype = {'ordem': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str, 'categoria_cnae': str}

    df = pd.read_csv(f'{filepath}', encoding='utf-8', dtype=dtype, usecols=cols)
    # df.columns = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label']
    return df


def get_label_name(int_key: int):
    if int_key in [cnae_scheme.scheme.undefined, cnae_scheme.scheme.undefined_labeled]:
        return "NÃO DEFINIDO"
    return cnae_scheme.scheme.get_label_with(int_key)


def label_data(L_train, label_method):
    if label_method == 's':
        label_model = LabelModel(cardinality=44, verbose=True)
        label_model.fit(L_train=L_train, n_epochs=500, log_freq=100, seed=args.seed)
        return label_model.predict(L_train)
    elif label_method == 'm':
        majority_model = MajorityLabelVoter()
        return majority_model.predict(L=L_train)
    else:
        preds = []
        for row in L_train:
            lf_output = -1
            lbl_func = 0
            while lf_output == -1 and lbl_func < len(row):
                lf_output = row[lbl_func]
                lbl_func += 1
            preds.append(lf_output)
        return preds


def main():
    # dists.test_dists()
    args = parse_args()
    df_train = import_csv(args.data_path)
    lfs = lf.get_lfs_list(args.edition_dist, args.phonetic_dist)

    print('Applying labeling functions...')
    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=df_train)

    if args.write_lfs:
        print('Writing labeling_funcs_output.txt...')
        with open('./output/0.25edition/labeling_funcs_output.txt', 'a+') as file:
            for index, row in df_train.iterrows():
                file.write(f'order: {row["order"]} | outputs: {L_train[index]}\n')

    with open('output/0.25edition/lfs-summary.txt', 'w') as f:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(f'{LFAnalysis(L=L_train, lfs=lfs).lf_summary()}\n', file=f)
    # print(df_train.iloc[L_train[:, 2] == poi_labels.scheme.wholesale_trade_except_motor_vehicles].sample(10, random_state=args.seed))

    preds = label_data(L_train, args.label_method)
    preds_readable = [get_label_name(p) for p in preds]

    print(f'Saving labeling to {args.output_path}...')
    df_train.assign(label=preds_readable, snorkel_category=preds).to_csv(args.output_path, index=False, encoding='utf-8')

    print('Done!')


# python3 label.py -w -e -p -l f -s 37625 -d input/sample-br-0.05-37625-semdup-manual-fix.csv -o output/labeled-sample-br-0.05-37625-semdup-manual-fix.csv
main()
