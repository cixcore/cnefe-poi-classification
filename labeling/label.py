import cnae_scheme as poi_labels
import cnefe_landuse_id_descriptions as cnefe_landuse_ids
import pandas as pd
from snorkel.labeling import labeling_function, PandasLFApplier, LFAnalysis
from snorkel.analysis import get_label_buckets
import argparse
import re


URBAN_LABEL = 1
RURAL_LABEL = 2


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--data_path', type=str, default='./shuffle-sample-BR-0.05-37625.csv', help='path to csv')
    parser.add_argument('-s', '--seed', type=int, default=37625,
                        help='defines seed to be used in sample.random_state to reproduce results')
    return parser.parse_args()


@labeling_function()
def farming_keywords(x):
    keywords = ['fazenda', 'plantio', 'plantacao', 'pecuaria', 'de corte', 'curral', 'ovelha']
    if (re.search(r'\bsitio\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bagric[uo]la\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcria(s|ss|c)ao\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcultivo\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcult(ura)? de\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcul(llt|l|it)?ivo\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcriame\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcriatorio\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bacude\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bgado', str(x.landuse_description), flags=re.I)
            or re.search(r'\bboi[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bvaca[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bsuino[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bporco[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\babelha[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\b[b]?ovin[oa][s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bpeixe[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bbode[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcabra[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bave[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bgalinha[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'[a-z]+cultura\b', str(x.landuse_description), flags=re.I)
            or any(keyword in str(x.landuse_description).lower() for keyword in keywords)
            or cnefe_landuse_ids.farming_establishment == int(x.landuse_id)):
        return poi_labels.scheme.farming
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def manufacturing_industries_keywords(x):
    keywords = ['abatedouro', 'frigorifico', 'abatedor', 'fabrica']
    if (re.search(r'\babate\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bconfec(c)?a[o0]\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bbarca(c|ss)a\b', str(x.landuse_description), flags=re.I)
            or any(keyword in str(x.landuse_description).lower() for keyword in keywords)):
        return poi_labels.scheme.manufacturing_industries
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def water_treatment_keywords(x):
    keywords = ['esgoto', 'tratamento de agua', 'departamento de agua', 'estacao de tratamento', 'distribuidora de agua']
    treatment_station_acronyms = ['dmae', 'corsan', 'agespisa', 'caesb']
    if (any(keyword in str(x.landuse_description).lower() for keyword in keywords)
            or any(acronym in str(x.landuse_description).lower() for acronym in treatment_station_acronyms)):
        return poi_labels.scheme.water_treatment
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def general_retail_keyword(x):
    if 'loja' == str(x.landuse_description).lower():
        return poi_labels.scheme.retail_and_motor_vehicle_repair_general
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def motor_vehicle_repair_and_retail_keywords(x):
    places = ['oficina', '0ficina', '0fissina', 'ofissina', 'mecanica']
    if any(place in str(x.landuse_description).lower() for place in places):
        return poi_labels.scheme.motor_vehicle_repair_and_retail
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def wholesale_trade_keyword(x):
    if 'atacado' in str(x.landuse_description).lower():
        return poi_labels.scheme.wholesale_trade_except_motor_vehicles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def ground_transportation_keywords(x):
    keywords = ['estacao de trem', 'estacao de metro', 'estacao rodoviaria', 'teleferico', 'moto taxi', 'mototaxi']
    if (any(keyword in str(x.landuse_description).lower() for keyword in keywords)
            or re.search(r'\btaxi\b', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.ground_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def water_transportation_keywords(x):
    keywords = ['catamara']
    if (any(keyword in str(x.landuse_description).lower() for keyword in keywords)
            or re.search(r'\bbalsa\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bbarc[oa]\b', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.water_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def air_transportation_keywords(x):
    keywords = ['aeroporto']
    if any(keyword in str(x.landuse_description).lower() for keyword in keywords):
        return poi_labels.scheme.air_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def storage_auxiliary_transport_activities_keywords(x):
    keywords = ['estacionamento']
    if any(keyword in str(x.landuse_description).lower() for keyword in keywords):
        return poi_labels.scheme.storage_auxiliary_transport_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def mail_and_other_delivery_services_keywords(x):
    keywords = ['correio']
    if any(keyword in str(x.landuse_description).lower() for keyword in keywords):
        return poi_labels.scheme.mail_and_other_delivery_services
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
    if re.search(r'\b(vag|vazi)[oa](s)?\b', str(x.landuse_description), flags=re.I) \
            or re.search(r'\bfechad[oa](s)?\b', str(x.landuse_description), flags=re.I) \
            or re.search(r'\bdesocupad[oa](s)?\b', str(x.landuse_description), flags=re.I):
        return poi_labels.scheme.vacant
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def undefined(x):
    if re.fullmatch(r'[0-9]*', str(x.landuse_description), flags=re.I):
        return poi_labels.scheme.undefined
    else:
        return poi_labels.scheme.undefined


def main():
    args = parse_args()
    df_train = pd.read_csv('shuffle-sample-BR-0.05-37625.csv', encoding='latin-1')
    print()

    lfs = [farming_keywords, general_retail_keyword, motor_vehicle_repair_and_retail_keywords, wholesale_trade_keyword,
           eating_places_keywords, education_keywords, churches_temples_religious_activities_keywords,
           vacant_keywords, undefined, vacant_keywords]

    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=df_train)
    # print(L_train)

    print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())
    # print(df_train.iloc[L_train[:, 2] == poi_labels.scheme.wholesale_trade_except_motor_vehicles].sample(10, random_state=args.seed))


# python3 sample.py -s 37625 -d shuffle-sample-BR-0.05-37625.csv
main()
