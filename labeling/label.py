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

    filename_open = 'sample-br-0.05-37625-semdup'  # 'shuffle-sample-BR-0.05-37625.csv', 'sample-br-0.05-37625-semduplic-reduced'
    filename_close = f'labeled-{filename_open}'

    parser.add_argument('-f', '--write_lfs', action='store_const', const=True, default=False,
                        help='write labeling funcs output to file')
    parser.add_argument('-d', '--data_path', type=str, default=f'./{filename_open}.csv', help='path to csv')
    parser.add_argument('-o', '--output_path', type=str, default=f'./{filename_close}.csv',
                        help='file to save labeling')
    parser.add_argument('-l', '--label_method', type=str, default='f',
                        help='label method to apply, can be <f>irst match, <s>norkel model, <m>ajority')
    parser.add_argument('-s', '--seed', type=int, default=37625,
                        help='defines seed to be used in sample.random_state to reproduce results')
    return parser.parse_args()


def import_csv(filepath):
    print(f'\nReading from file "{filepath}"...')
    dtype = {'ordem': int, 'uf': int, 'municipality': int, 'district': int, 'sub_district': int, 'urban_rural': int,
             'landuse_id': int, 'landuse_description': str, 'categoria_cnae': str}
    df = pd.read_csv(f'{filepath}', encoding='utf-8',
                     usecols=['ordem', 'uf', 'municipality', 'district', 'sub_district', 'urban_rural', 'landuse_id',
                              'landuse_description', 'categoria_cnae'], dtype=dtype)
    df.columns = ['order', 'uf', 'municipality', 'district', 'sub_district', 'urban_rural',
                  'landuse_id', 'landuse_description', 'manual_label']
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
            size = len(preds)
            for lf_output in row:
                if lf_output != -1:
                    preds.append(lf_output)
                    break
            if len(preds) == size:
                preds.append(-1)
        return preds


def main():
    # dists.test_dists()
    args = parse_args()
    df_train = import_csv(args.data_path)
    lfs = lf.lfs_list

    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=df_train)

    if args.write_lfs:
        print('Writing labeling_funcs_output.txt...')
        with open('labeling_funcs_output.txt', 'a+') as file:
            for index, row in df_train.iterrows():
                file.write(f'order: {row["order"]} | outputs: {L_train[index]}\n')

    print(f'{LFAnalysis(L=L_train, lfs=lfs).lf_summary()}\n')
    # print(df_train.iloc[L_train[:, 2] == poi_labels.scheme.wholesale_trade_except_motor_vehicles].sample(10, random_state=args.seed))

    preds = label_data(L_train, args.label_method)
    preds_readable = [get_label_name(p) for p in preds]

    print(f'Saving labeling to {args.data_path}...')
    df_train.assign(label=preds_readable, snorkel_category=preds).to_csv(args.output_path, index=False, encoding='utf-8')

    print('Done!')


# python3 label.py -s 37625 -d shuffle-sample-BR-0.05-37625.csv -l f
main()
