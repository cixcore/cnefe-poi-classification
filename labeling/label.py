import ordnancesurvey_poi_scheme as poi_labels
import pandas as pd
from snorkel.labeling import labeling_function, PandasLFApplier, LFAnalysis


@labeling_function()
def oficina(x):
    return poi_labels.repair_and_servicing if "oficina" in str(x.landuse_description).lower() else -1


@labeling_function()
def bar(x):
    return poi_labels.eating_and_drinking if "bar" in str(x.landuse_description).lower() else -1


def main():
    df_train = pd.read_csv('cnefe_amostra.csv')
    lfs = [oficina, bar]

    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=df_train)
    # print(L_train)

    print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())
    print(df_train.iloc[L_train[:, 0] == poi_labels.repair_and_servicing].landuse_description.sample(10, random_state=1))


main()
