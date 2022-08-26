import pandas as pd
from snorkel.labeling import PandasLFApplier, LFAnalysis
from snorkel.labeling.model import LabelModel, MajorityLabelVoter
from snorkel.analysis import get_label_buckets
import cnae_scheme
import argparse
import json
import lf


def parse_args():
    parser = argparse.ArgumentParser()

    filename_open = 'sample-br-0.05-37625-semdup-manual-fix'
    filename_close = f'labeled-{filename_open}'
    folder = 'dists'

    parser.add_argument('-w', '--write_lfs', action='store_const', const=True, default=False,
                        help='write labeling funcs output to file')
    parser.add_argument('-e', '--edition_dist', action='store_const', const=True, default=False,
                        help='use levenshtein distance with qwerty wights functions')
    parser.add_argument('-p', '--phonetic_dist', action='store_const', const=True, default=False,
                        help='use portuguese soundex distance functions')
    parser.add_argument('-d', '--data_path', type=str, default=f'./input/{filename_open}.csv', help='path to csv')
    parser.add_argument('-o', '--output_path', type=str, default=f'./output/{folder}/{filename_close}.csv',
                        help='file to save labeling')
    parser.add_argument('-f', '--folder_output_path', type=str, default=folder, help='dir to save auxilary outputs')
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


def get_func_name(args, func_index):
    if args.edition_dist and args.phonetic_dist:
        return lf.all_lfs_dict[func_index+1]
    elif args.edition_dist:
        return lf.lfs_with_edit_dists[func_index+1]
    elif args.phonetic_dist:
        return lf.lfs_with_phonetic_dists[func_index+1]


def main():
    args = parse_args()
    df_train = import_csv(args.data_path)
    lfs = lf.get_lfs_list(args.edition_dist, args.phonetic_dist)

    print('Applying labeling functions...')
    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=df_train)

    with open(f'output/{args.folder_output_path}/lfs-summary.txt', 'w') as f:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(f'{LFAnalysis(L=L_train, lfs=lfs).lf_summary()}\n', file=f)
    # print(df_train.iloc[L_train[:, 2] == poi_labels.scheme.wholesale_trade_except_motor_vehicles].sample(10, random_state=args.seed))

    preds = label_data(L_train, args.label_method)
    preds_readable = [get_label_name(p) for p in preds]

    print(f'Saving labeling to {args.output_path}...')
    df_train.assign(pred_label=preds_readable, snorkel_category=preds).to_csv(args.output_path, index=False, encoding='utf-8')

    if args.write_lfs:
        print('Writing labeling_funcs_output_readable.json...')
        with open(f'./output/{args.folder_output_path}/labeling_funcs_output_readable.json', 'a+') as file:
            json_arr = []
            for index, row in df_train.iterrows():
                outputs = []
                for func_index, func_output in enumerate(L_train[index]):
                    if func_output != -1:
                        outputs.append(get_func_name(args, func_index))
                json_obj = {
                    'order': row['order'],
                    'outputs': outputs
                }
                json_arr.append(json_obj)
            file.write(json.dumps(json_arr))
    print('Done!')

# python3 label.py -w -e -p -f with-dists -l f -s 37625 -d input/sample-br-0.05-37625-semdup-manual-fix.csv -o output/with-dists/labeled-sample-br-0.05-37625-semdup-manual-fix.csv
# python3 label.py -w -f no-dists -l f -s 37625 -d input/sample-br-0.05-37625-semdup-manual-fix.csv -o output/no-dists/labeled-no-dists-semdup-manual-fix.csv

# python3 label.py -w -e -f no-manual/just-edit -l f -s 37625 -d input/sample-br-0.05-37625-semdup-manual-fix.csv -o output/no-manual/just-edit/labeled-br-0.05-37625.csv
# python3 label.py -w -p -f no-manual/just-phonetic -l f -s 37625 -d input/sample-br-0.05-37625-semdup-manual-fix.csv -o output/no-manual/just-phonetic/labeled-br-0.05-37625.csv


main()
