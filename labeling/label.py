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
def farming_keywords(x):
    keywords = ['fazenda', 'plantio', 'plantacao', 'pecuaria', 'cultura de']
    if (re.search(r'\bsitio\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcriacao\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcultivo\b', str(x.landuse_description), flags=re.I)
            or re.search(r'[a-z]+cultura\b', str(x.landuse_description), flags=re.I)
            or any(keyword in str(x.landuse_description).lower() for keyword in keywords)
            or cnefe_landuse_ids.farming_establishment == int(x.landuse_id)):
        return poi_labels.scheme.eating_places
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def general_retail_keyword(x):
    if 'loja' == str(x.landuse_description).lower():
        return poi_labels.scheme.retail_and_motor_vehicle_repair_general
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def wholesale_trade_keyword(x):
    if 'atacado' in str(x.landuse_description).lower():
        return poi_labels.scheme.wholesale_trade_except_motor_vehicles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def motor_vehicle_repair_and_retail_keywords(x):
    if any(place in str(x.landuse_description).lower() for place in ['oficina', 'mecanica']):
        return poi_labels.scheme.motor_vehicle_repair_and_retail
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def eating_places_keywords(x):
    common_foods = ['pizza', 'hamburgue', 'sushi', 'pastel', 'pasteis', 'sorvete']
    common_places = ['lanche', 'lanchonete', 'boteco', 'cafeteria', 'restaurante']
    if re.search(r'\bbar\b', str(x.landuse_description), flags=re.I) \
            or any(place in str(x.landuse_description).lower() for place in common_places) \
            or any(food in str(x.landuse_description).lower() for food in common_foods):
        return poi_labels.scheme.eating_places
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def education_keywords(x):
    keywords = ['escola', 'colegio', 'faculdade', 'universidade', 'creche', 'ensino']
    if (any(keyword in str(x.landuse_description).lower() for keyword in keywords)
            or cnefe_landuse_ids.educational_establishment == int(x.landuse_id)):
        return poi_labels.scheme.education
    else:
        return poi_labels.scheme.undefined


""" 
'educacao' ('educação') generated too many false positives (syndicates, 
governmental institutions, etc) and some true positives already covered in the other conditions
--------------------------------------------------------------
| landuse_id     | landuse_description                       |
--------------------------------------------------------------
| 6              | EDUCACAO INFANTIL COLEGIO LONDRINENSE     |
| 6              | SECRETARIA DE EDUCACAO                    | 
| 4              | UNIDADE EDUCACAO BASICA HAYDEE CHAVES     |
| 6              | SECRETARIA DE EDUCACAO                    |
| 4              | CENTRO DE EDUCACAO PROFISSIONAL EM ARTES  |
| 6              | DEPOSITO PREF EDUCACAO                    |
| 6              | SECRETARIA DE EDUCACAO                    |
| 4              | UNIDADE DE EDUCACAO INFANTIL EDNA LIMA M  |
| 6              | ESCOLA DE EDUCACAO INFANTIL               |
| 4              | INTEGRADO DE EDUCACAO ESPECIAL           [...]
--------------------------------------------------------------
@labeling_function()
def education_word(x):
    if 'educacao' in str(x.landuse_description).lower():
        return poi_labels.scheme.education
    else:
        return poi_labels.scheme.undefined
"""


@labeling_function()
def churches_temples_religious_activities_keywords(x):
    has_entities = (re.search(r'\bdeus\b', str(x.landuse_description), flags=re.I)
                    or re.search(r'\bjesus\b', str(x.landuse_description), flags=re.I)
                    or re.search(r'\bcristo\b', str(x.landuse_description), flags=re.I)
                    or 'nossa senhora' in str(x.landuse_description).lower()
                    or re.search(r'\bogum\b', str(x.landuse_description), flags=re.I)
                    or re.search(r'\biemanja\b', str(x.landuse_description), flags=re.I)
                    or re.search(r'\bexu\b', str(x.landuse_description), flags=re.I)
                    or re.search(r'\boxum\b', str(x.landuse_description), flags=re.I)
                    or re.search(r'\boxala\b', str(x.landuse_description), flags=re.I)
                    or re.search(r'\bxango\b', str(x.landuse_description), flags=re.I)
                    or re.search(r'\bomulu\b', str(x.landuse_description), flags=re.I)
                    or re.search(r'\borixa', str(x.landuse_description), flags=re.I))
    if int(x.landuse_id) not in [cnefe_landuse_ids.educational_establishment, cnefe_landuse_ids.health_establishment] \
            and ('igreja' in str(x.landuse_description).lower() or 'templo' in str(x.landuse_description).lower()
                 or re.search(r'\bespirit(a|o|ual)\b', str(x.landuse_description), flags=re.I)
                 or re.search(r'\bcatolic[oa]\b', str(x.landuse_description), flags=re.I)
                 or re.search(r'\bevangelic[oa]\b', str(x.landuse_description), flags=re.I)
                 or 'umbanda' in str(x.landuse_description).lower() or 'candomble' in str(x.landuse_description).lower()
                 or 'judaica' in str(x.landuse_description).lower() or 'batista' in str(x.landuse_description).lower()
                 or 'capela' in str(x.landuse_description).lower() or 'catedral' in str(x.landuse_description).lower()
                 or 'evangel' in str(x.landuse_description).lower() or has_entities):
        return poi_labels.scheme.churches_temples_religious_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def vacant_keywords(x):
    if 'desocupad' in str(x.landuse_description).lower() \
            or re.search(r'\b(vag|vazi)[oa]\b', str(x.landuse_description), flags=re.I):
        return poi_labels.scheme.vacant
    else:
        return poi_labels.scheme.undefined


def main():
    args = parse_args()
    df_train = pd.read_csv('shuffle-sample-BR-0.05-37625.csv', encoding='latin-1')
    print()

    lfs = [farming_keywords, general_retail_keyword, motor_vehicle_repair_and_retail_keywords, wholesale_trade_keyword,
           eating_places_keywords, education_keywords, churches_temples_religious_activities_keywords,
           vacant_keywords]

    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=df_train)
    # print(L_train)

    print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())
    # print(df_train.iloc[L_train[:, 2] == poi_labels.scheme.wholesale_trade_except_motor_vehicles].sample(10, random_state=args.seed))


# python3 sample.py -s 37625 -d shuffle-sample-BR-0.05-37625.csv
main()
