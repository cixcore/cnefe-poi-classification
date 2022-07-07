import cnae_scheme as poi_labels
import cnefe_landuse_id_descriptions as cnefe_landuse_ids
import pandas as pd
from snorkel.labeling import labeling_function, PandasLFApplier, LFAnalysis
from snorkel.analysis import get_label_buckets
import argparse
import re


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--data_path', type=str, default='./shuffle-sample-BR-0.05-37625.csv', help='path to csv')
    parser.add_argument('-s', '--seed', type=int, default=37625,
                        help='defines seed to be used in sample.random_state to reproduce results')
    return parser.parse_args()


@labeling_function()
def motor_vehicle_repair_and_retail_keywords(x):
    if "oficina" in str(x.landuse_description).lower():
        return poi_labels.scheme.motor_vehicle_repair_and_retail
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def eating_places_keywords(x):
    if re.search(r"\bbar\b", str(x.landuse_description), flags=re.I) \
            or "lanche" in str(x.landuse_description).lower() \
            or "lanchonete" in str(x.landuse_description).lower() \
            or "restaurante" in str(x.landuse_description).lower():
        return poi_labels.scheme.eating_places
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def vacant_keywords(x):
    if "desocupad" in str(x.landuse_description).lower() \
            or re.search(r"\bvag[oa]\b", str(x.landuse_description), flags=re.I):
        return poi_labels.scheme.vacant
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def education_keywords(x):
    # 'educação' generated too many false positives (syndicates, governmental institutions, etc)
    # and cases covered in the other conditions
    if "escola" in str(x.landuse_description).lower() \
            or "colegio" in str(x.landuse_description).lower() \
            or "ensino" in str(x.landuse_description).lower() \
            or "faculdade" in str(x.landuse_description).lower() \
            or "universidade" in str(x.landuse_description).lower() \
            or "creche" in str(x.landuse_description).lower() \
            or cnefe_landuse_ids.educational_establishment == int(x.landuse_id):
        return poi_labels.scheme.education
    else:
        return poi_labels.scheme.undefined


""" 
'educacao' ('educação') generated too many false positives 
(syndicates, governmental institutions, etc) and some true positives already covered in the other conditions
------------------------------------------------------------
landuse_id      landuse_description
------------------------------------------------------------
6               EDUCACAO INFANTIL COLEGIO LONDRINENSE
6               SECRETARIA DE EDUCACAO
4               UNIDADE EDUCACAO BASICA HAYDEE CHAVES
6               SECRETARIA DE EDUCACAO
4               CENTRO DE EDUCACAO PROFISSIONAL EM ARTES
6               DEPOSITO PREF EDUCACAO
6               SECRETARIA DE EDUCACAO
4               UNIDADE DE EDUCACAO INFANTIL EDNA LIMA M
6               ESCOLA DE EDUCACAO INFANTIL
4               INTEGRADO DE EDUCACAO ESPECIAL
------------------------------------------------------------
@labeling_function()
def education_word(x):
    if "educacao" in str(x.landuse_description).lower():
        return poi_labels.scheme.education
    else:
        return poi_labels.scheme.undefined
"""


@labeling_function()
def churches_temples_religious_activities_keywords(x):
    if int(x.landuse_id) not in [cnefe_landuse_ids.educational_establishment, cnefe_landuse_ids.health_establishment] \
            and ("igreja" in str(x.landuse_description).lower()
                 or re.search(r"\bdeus\b", str(x.landuse_description), flags=re.I)
                 or re.search(r"\bjesus\b", str(x.landuse_description), flags=re.I)
                 or "umbanda" in str(x.landuse_description).lower()
                 or "templo" in str(x.landuse_description).lower()
                 or "nossa senhora" in str(x.landuse_description).lower()
                 or "batista" in str(x.landuse_description).lower()):
        return poi_labels.scheme.churches_temples_religious_activities
    else:
        return poi_labels.scheme.undefined


def main():
    args = parse_args()
    df_train = pd.read_csv('shuffle-sample-BR-0.05-37625.csv', encoding='latin-1')
    print()

    lfs = [eating_places_keywords, motor_vehicle_repair_and_retail_keywords, vacant_keywords, education_keywords,
           churches_temples_religious_activities_keywords]

    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=df_train)
    # print(L_train)

    print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())
    print(df_train.iloc[L_train[:, 3] == poi_labels.scheme.education].sample(10, random_state=args.seed))


# python3 sample.py -s 37625 -d shuffle-sample-BR-0.05-37625.csv
main()
