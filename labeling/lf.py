import cnae_scheme as poi_labels
import cnefe_landuse_id_descriptions as cnefe_landuse_ids
import re
from snorkel.labeling import labeling_function

URBAN_LABEL = 1
RURAL_LABEL = 2


def regex_match_in_list(items_list, x):
    return any(re.search(rf'\b{item}\b', str(x.landuse_description), flags=re.I) for item in items_list)


def regex_match_word(word, x):
    return re.search(rf'\b{word}\b', str(x.landuse_description), flags=re.I)


def match_any_item_in_list(keywords, x):
    return any(keyword in str(x.landuse_description).lower() for keyword in keywords)


def match_all_items(keywords, x):
    return all(keyword in str(x.landuse_description).lower() for keyword in keywords)


@labeling_function()
def farming_keywords(x):
    keywords = ['fazenda', 'plantio', 'plantacao', 'pecuaria',
                'de corte', 'curral', 'ovelha', 'aviario', 'galpao', 'granja']
    if (re.search(r'\bagric[uo]la\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcria(s|ss|c)ao\b', str(x.landuse_description), flags=re.I)
            or regex_match_word('criame', x) or regex_match_word('cultivo', x)
            or regex_match_word('criatorio', x) or regex_match_word('acude', x)
            or regex_match_word('gado', x) or regex_match_word('sitio', x)
            or regex_match_word('fumo', x) or regex_match_word('estufa', x)
            or re.search(r'\bcult(ura)? de\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcul(llt|l|it)?ivo\b', str(x.landuse_description), flags=re.I)
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
            or re.search(r'\bgalinh(a|eiro)[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcavalo[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bcurral[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bgranja[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\b(ch|x)iqueiro[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'[a-z]+cultura\b', str(x.landuse_description), flags=re.I)
            or match_any_item_in_list(keywords, x)
            or cnefe_landuse_ids.farming_establishment == int(x.landuse_id)):
        return poi_labels.scheme.farming
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def extractive_industries_keywords(x):
    keywords = ['extracao de', 'marmore', 'garimpo', 'mineracao', 'metais preciosos',
                'manganes', 'titanio', 'niobio', 'aluminio']
    if (re.search(r'\bmine(i)?radora\b', str(x.landuse_description), flags=re.I)
            or regex_match_word('carvao', x) or regex_match_word('minerio', x)
            or regex_match_word('cobre', x) or regex_match_word('estanho', x)
            or regex_match_word('areia', x) or regex_match_word('argila', x)
            or match_any_item_in_list(keywords, x)):
        return poi_labels.scheme.extractive_industries
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def manufacturing_industries_keywords(x):
    keywords = ['abatedouro', 'frigorifico', 'abatedor', 'fabrica', 'confeccoes']
    if (regex_match_word('abate', x) or match_any_item_in_list(keywords, x)
            or re.search(r'\bconfec(c)?a[o0]\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bbarca(c|ss)a\b', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.manufacturing_industries
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def gas_and_electricity_keywords(x):
    keywords = ['eletricidade', 'energia', 'energetica']
    energy_station_names_and_acronyms = ['ceee', 'cpfl', 'cesp', 'rge', 'aes', 'auren', 'ccee', 'cresesb',
                                         'cerbranorte', 'ceriluz', 'edp', 'endesa', 'enel', 'energisa',
                                         'enerpeixe', 'eneva', 'engie', 'neoenergia']
    if (match_any_item_in_list(keywords, x) or regex_match_in_list(energy_station_names_and_acronyms, x)
            or re.search(r'\bga[sz]\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bsub\s?estacao\b', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.gas_and_electricity
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def water_treatment_keywords(x):
    keywords = ['esgoto', 'tratamento de agua', 'departamento de agua', 'estacao de tratamento',
                'distribuidora de agua']
    treatment_station_acronyms = ['dmae', 'corsan', 'agespisa', 'caesb']
    if match_any_item_in_list(keywords, x) or regex_match_in_list(treatment_station_acronyms, x):
        return poi_labels.scheme.water_treatment
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def construction_keywords(x):
    keywords = ['empresa de construcao', 'incorporadora', 'construcoes', 'incorporacao', 'empreiteira']
    if match_all_items(['construcao', 'engenharia'], x) or match_any_item_in_list(keywords, x):
        return poi_labels.scheme.construction
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def motor_vehicle_repair_and_retail_keywords(x):
    places = ['oficina', '0ficina', '0fissina', 'ofissina', 'mecanica']
    keywords = ['martelinho de ouro', 'automotivo', 'motor', 'veiculo']
    if (match_any_item_in_list(places, x) or match_any_item_in_list(keywords, x) or regex_match_word('auto', x)
            or re.search(r'\bpneu[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\brodas[s]?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bfun[ei]laria[s]?\b', str(x.landuse_description), flags=re.I)):
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
def non_specialized_retail_trade_keyword(x):
    if (match_all_items(['loja', 'departamento'], x)
            or 'variedade' in str(x.landuse_description).lower()
            or 'utilidade' in str(x.landuse_description).lower()
            or 'loja' == str(x.landuse_description).lower()):
        return poi_labels.scheme.non_specialized_retail_trade
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def non_specialized_retail_foodstuffs_supermarkets_keyword(x):
    keywords = ['supermercado', 'mercadao', 'hipermercado']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.non_specialized_retail_foodstuffs_supermarkets
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def non_specialized_retail_foodstuffs_grocery_stores_keyword(x):
    keywords = ['mercearia', 'armazem']
    if (match_any_item_in_list(keywords, x)
            or re.search(r'\b(min[ie]\s?)?mercado', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.non_specialized_retail_foodstuffs_grocery_stores
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_food_beverages_tobacco_keyword(x):
    keywords = ['padaria', 'acougue', 'casa de carne', 'tabacaria', 'bebidas']
    if (match_any_item_in_list(keywords, x) or match_all_items(['distribuidora', 'bebidas'], x)
            or re.search(r'\bconfe(i)?taria\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bpe(i)?xaria\b', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.retail_food_beverages_tobacco
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_fuel_keyword(x):
    keywords = ['gasolina', 'ipiranga', 'auto posto', 'texaco', 'diesel']
    if (match_any_item_in_list(keywords, x) or regex_match_word('br', x) or regex_match_word('shell', x)
            or re.search(r'\bcombustive(l|is)\b', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.retail_fuel
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_building_material_keyword(x):
    if re.search(r'\bmateria(l|is) de construcao\b', str(x.landuse_description), flags=re.I):
        return poi_labels.scheme.retail_building_material
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_computer_communication_household_equipment_keyword(x):
    keywords = ['armarinho', 'mesa e banho', 'eletrodomesticos', 'moveis']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.retail_computer_communication_household_equipment
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_sport_culture_recreation_articles_keyword(x):
    keywords = ['livraria', 'papelaria', 'loja de esportes', 'loja de brinquedo']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.retail_sport_culture_recreation_articles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_keyword(x):
    keywords = ['boticario', 'cosmetico', 'farmacia', 'drogaria', 'oculos', 'otica', 'ortopedico']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_new_products_non_specified_previously_and_second_hand_keyword(x):
    keywords = ['roupas', 'roupas intimas', 'bijoux', 'fashion', 'presentes', 'calcados', 'bazar', 'jeans',
                'brecho', 'loja de relogios', 'joalheria', 'floricultura', 'antiquario', 'antiguidades']
    if (match_any_item_in_list(keywords, x)
            or re.search(r'\bro(u|p|up)a(s)?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bmalha(s)?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bmoda(s)?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bl[iae]ngerie\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bbij(o|u|ou)teria\b', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.retail_new_products_non_specified_previously_and_second_hand
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def ground_transportation_keywords(x):
    keywords = ['estacao de trem', 'estacao de metro', 'estacao rodoviaria', 'teleferico', 'moto taxi', 'mototaxi']
    if match_any_item_in_list(keywords, x) or regex_match_word('taxi', x):
        return poi_labels.scheme.ground_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def water_transportation_keywords(x):
    keywords = ['catamara']
    if (match_any_item_in_list(keywords, x) or regex_match_word('balsa', x)
            or re.search(r'\bbarc[oa]\b', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.water_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def air_transportation_keywords(x):
    keywords = ['aeroporto']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.air_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def storage_auxiliary_transport_activities_keywords(x):
    keywords = ['estacionamento', 'galpao', 'paiol', 'tulha', 'deposito', 'logistica', 'armazena']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.storage_auxiliary_transport_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def mail_and_other_delivery_services_keywords(x):
    keywords = ['correio', 'fedex', 'sedex']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.mail_and_other_delivery_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def accommodation_keywords(x):
    keywords = ['hotel', 'pousada', 'hospedaria', 'hospedagem']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.accommodation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def eating_places_keywords(x):
    common_foods = ['pizza', 'hamburgue', 'sushi', 'pastel', 'pasteis', 'sorvete', 'churrasc']
    common_places = ['lanche', 'lanchonete', 'boteco', 'cafeteria', 'restaurante']
    if (regex_match_word('bar', x)
            or match_any_item_in_list(common_places, x) or match_any_item_in_list(common_foods, x)):
        return poi_labels.scheme.eating_places
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def information_and_communication_keywords(x):
    keywords = ['software', 'estudio', 'informatica']
    internet_providers = ['oi', 'tim', 'net', 'claro', 'vivo', 'gvt', 'embratel']
    if (regex_match_word('grafica', x)
            or re.search(r'\blan\s?house\b', str(x.landuse_description), flags=re.I)
            or match_any_item_in_list(keywords, x) or regex_match_in_list(internet_providers, x)):
        return poi_labels.scheme.information_and_communication
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def financial_activities_insurance_keywords(x):
    keywords = ['banco', 'seguro']
    banks = ['santander', 'bradesco', 'banco do brasil', 'itau', 'caixa', 'banrisul']
    if match_any_item_in_list(keywords, x) or regex_match_in_list(banks, x):
        return poi_labels.scheme.financial_activities_insurance
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def real_estate_activities_keywords(x):
    keywords = ['imobiliaria']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.real_estate_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def professional_scientific_and_technic_activities_keywords(x):
    keywords = ['cartorio', 'tabeliao', 'tabelionato', 'registro civil', 'juizado'
                'oficio de notas', 'despachante', 'escritorio de', 'advocacia', 'advogad', 'contador']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.professional_scientific_and_technic_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def administrative_activities_complementary_services_keywords(x):
    keywords = ['loteria', 'loterica', 'aluguel de carro', 'locacao de automove', 'agencia de turismo']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.administrative_activities_complementary_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def public_administration_social_security_defence_keywords(x):
    keywords = ['prefeitura', 'delegacia', 'batalhao', 'centro administrativo', 'militar', 'policia', 'vara civel', 'civil']
    if match_any_item_in_list(keywords, x) or regex_match_in_list(['dp', 'bpm', 'detran', 'contran', 'ciretran'], x):
        return poi_labels.scheme.public_administration_social_security_defence
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
def education_keywords(x):
    keywords = ['escola', 'colegio', 'faculdade', 'universidade', 'creche', 'ensino', 'formacao', 'formacao de condutores']
    if (match_any_item_in_list(keywords, x) or regex_match_word('cfc', x)
            or cnefe_landuse_ids.educational_establishment == int(x.landuse_id)):
        return poi_labels.scheme.education
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def human_health_social_services_keywords(x):
    keywords = ['consultorio', 'cardiologista', 'dentista', 'odonto', 'psicolog', 'fisioterap', 'terapia'
                'diagnostico', 'pronto socorro', 'hospital', 'hospicio', 'medic', 'assistencia']
    if (match_any_item_in_list(keywords, x)
            or cnefe_landuse_ids.health_establishment == int(x.landuse_id)):
        return poi_labels.scheme.human_health_social_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def arts_culture_sport_recreation_keywords(x):
    keywords = ['teatro', 'museu', 'biblioteca', 'clube social', 'cassino',
                'complexo esportivo', 'ginasio', 'esportivo', 'brinquedoteca']
    if match_any_item_in_list(keywords, x) or regex_match_in_list(['praca', 'parque'], x):
        return poi_labels.scheme.arts_culture_sport_recreation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def international_organisms_other_extraterritorial_institutions_keywords(x):
    keywords = ['consulado', 'embaixada']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.international_organisms_other_extraterritorial_institutions
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def other_service_activities_keywords(x):
    keywords = ['cabeleireiro', 'barbearia', 'manicure', 'tatuagem', 'alfaiate',
                'costureira', 'fotografo', 'salao de', 'hotel para ', 'reparo']
    if (match_any_item_in_list(keywords, x)
            or re.search(r'\bcabe[rl]e(i)?[lr]e(i)?r[oa](s)?\b', str(x.landuse_description),
                         flags=re.I)  # cabeleireiro, cabelerero, cabeleleiro, cabelelero
            or re.search(r'\bcabe[rl]e(i)?r[oa](s)?\b', str(x.landuse_description), flags=re.I)  # cabeleiro
            or re.search(r'\bbele[sz]a?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bta(t)*oo\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bpet\s?shop\b', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.other_service_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def churches_temples_religious_activities_keywords(x):
    has_entities = (regex_match_word('deus', x) or regex_match_word('jesus', x)
                    or regex_match_word('cristo', x) or regex_match_word('ogum', x)
                    or regex_match_word('iemanja', x) or regex_match_word('exu', x)
                    or regex_match_word('oxum', x) or regex_match_word('oxala', x)
                    or regex_match_word('xango', x) or regex_match_word('omulu', x)
                    or regex_match_word('orixa', x) or 'nossa senhora' in str(x.landuse_description).lower())
    if (int(x.landuse_id) not in [cnefe_landuse_ids.educational_establishment, cnefe_landuse_ids.health_establishment]
            and ('igreja' in str(x.landuse_description).lower() or 'templo' in str(x.landuse_description).lower()
                 or re.search(r'\bespirit(a|o|ual|ualidade)\b', str(x.landuse_description), flags=re.I)
                 or re.search(r'\bcatolic[oa]\b', str(x.landuse_description), flags=re.I)
                 or re.search(r'\bevangelic[oa]\b', str(x.landuse_description), flags=re.I)
                 or 'umbanda' in str(x.landuse_description).lower() or 'candomble' in str(x.landuse_description).lower()
                 or 'judaica' in str(x.landuse_description).lower() or 'batista' in str(x.landuse_description).lower()
                 or 'capela' in str(x.landuse_description).lower() or 'catedral' in str(x.landuse_description).lower()
                 or 'sinagoga' in str(x.landuse_description).lower() or 'catequetico' in str(
                        x.landuse_description).lower()
                 or 'evangel' in str(x.landuse_description).lower() or has_entities)):
        return poi_labels.scheme.churches_temples_religious_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def vacant_keywords(x):
    if (match_any_item_in_list(['baldio', 'inoperante'], x)
            or re.search(r'\b(vag|vazi)[oa](s)?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bfechad[oa](s)?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bdesocupad[oa](s)?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\babandonad[oa](s)?\b', str(x.landuse_description), flags=re.I)
            or re.search(r'\bantig[oa]\b', str(x.landuse_description), flags=re.I)):
        return poi_labels.scheme.vacant
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def undefined(x):
    if re.fullmatch(r'[0-9]*', str(x.landuse_description), flags=re.I):
        return poi_labels.scheme.undefined_labeled
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def use_manual_label(x):
    if str(x.cnae_category) == 'nan':
        return poi_labels.scheme.undefined
    else:
        for key in poi_labels.scheme.name_to_label_2way:
            if type(key) is str:
                if str(key).lower() in str(x.cnae_category).lower():
                    return poi_labels.scheme.name_to_label_2way[key]
    return poi_labels.scheme.undefined


@labeling_function()
def use_manual_label_1(x):
    return use_manual_label(x)


@labeling_function()
def use_manual_label_2(x):
    return use_manual_label(x)


@labeling_function()
def use_manual_label_3(x):
    return use_manual_label(x)


lfs_dict = {
    0: use_manual_label_1,
    1: use_manual_label_2,
    2: use_manual_label_3,
    3: farming_keywords,
    4: extractive_industries_keywords,
    5: manufacturing_industries_keywords,
    6: gas_and_electricity_keywords,
    7: water_treatment_keywords,
    8: construction_keywords,
    9: motor_vehicle_repair_and_retail_keywords,
    10: wholesale_trade_keyword,
    11: non_specialized_retail_trade_keyword,
    12: non_specialized_retail_foodstuffs_supermarkets_keyword,
    13: non_specialized_retail_foodstuffs_grocery_stores_keyword,
    14: retail_food_beverages_tobacco_keyword,
    15: retail_fuel_keyword,
    16: retail_building_material_keyword,
    17: retail_computer_communication_household_equipment_keyword,
    18: retail_sport_culture_recreation_articles_keyword,
    19: retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_keyword,
    20: retail_new_products_non_specified_previously_and_second_hand_keyword,
    21: ground_transportation_keywords,
    22: water_transportation_keywords,
    23: air_transportation_keywords,
    24: storage_auxiliary_transport_activities_keywords,
    25: mail_and_other_delivery_services_keywords,
    26: accommodation_keywords,
    27: eating_places_keywords,
    28: information_and_communication_keywords,
    29: financial_activities_insurance_keywords,
    30: real_estate_activities_keywords,
    31: professional_scientific_and_technic_activities_keywords,
    32: administrative_activities_complementary_services_keywords,
    33: public_administration_social_security_defence_keywords,
    34: education_keywords,
    35: human_health_social_services_keywords,
    36: arts_culture_sport_recreation_keywords,
    37: international_organisms_other_extraterritorial_institutions_keywords,
    38: other_service_activities_keywords,
    39: churches_temples_religious_activities_keywords,
    40: vacant_keywords,
    41: undefined
}
