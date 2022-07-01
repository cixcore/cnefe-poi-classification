import ordnancesurvey_poi_scheme as poi_labels
import pandas as pd
from snorkel.labeling import labeling_function, PandasLFApplier, LFAnalysis
import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--data_path', type=str, default='./sample-BR-0.05.csv', help='path to csv')
    parser.add_argument('-s', '--seed', type=int, default=0,
                        help='defines seed to be used in sample.random_state to reproduce results')
    return parser.parse_args()


@labeling_function()
def oficina(x):
    return poi_labels.repair_and_servicing if "oficina" in str(x.landuse_description).lower() else -1


@labeling_function()
def bar(x):
    return poi_labels.eating_and_drinking if "bar" in str(x.landuse_description).lower() else -1


def main():
    args = parse_args()
    df_train = pd.read_csv('cnefe_amostra.csv')
    lfs = [oficina, bar]

    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=df_train)
    # print(L_train)

    print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())
    print(df_train.iloc[L_train[:, 0] == poi_labels.repair_and_servicing].landuse_description.sample(10, random_state=args.seed))


# python3 sample.py -s 37625 -d sample-BR-0.05-37625.csv
main()
