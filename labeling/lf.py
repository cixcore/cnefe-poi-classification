import cnae_scheme as poi_labels
import cnefe_landuse_id_descriptions as cnefe_landuse_ids
import re
from snorkel.labeling import labeling_function
from word_dists import dists

URBAN_LABEL = 1
RURAL_LABEL = 2


def description(x):
    # print(x.order)
    return re.sub(r'[^a-zA-Z0-9\s]', '',
                  re.sub(r'[áãâà]', 'a',
                         re.sub(r'[éẽê3]', 'e',
                                re.sub(r'[íĩî1]', 'i',
                                       re.sub(r'[óõô0]', 'o',
                                              re.sub(r'[úũûü]', 'u',
                                                     re.sub(r'[ç]', 'c', str(x.landuse_description).lower())))))))


def regex_match_in_list(items_list, x):
    return any(re.search(rf'\b{item}\b', description(x), flags=re.I) for item in items_list)


def regex_match_word(word, x):
    return re.search(rf'\b{word}\b', description(x), flags=re.I)


def match_any_item_in_list(keywords, x):
    return any(keyword in description(x) for keyword in keywords)


def match_all_items(keywords, x):
    return all(keyword in description(x) for keyword in keywords)


def aviamentos_urban_rural(x, urban_rural):
    if 'aviamentos' in description(x) and urban_rural == x.urban_rural:
        return True
    return False


@labeling_function()
def farming_keywords(x):
    keywords = ['fazenda', 'plantio', 'plantacao', 'pecuaria',
                'de corte', 'curral', 'ovelha', 'aviario', 'galpao', 'granja']
    if (re.search(r'\bagric[uo]la(s)?\b', description(x), flags=re.I)
            or re.search(r'\bcria(s|ss|c)ao\b', description(x), flags=re.I)
            or regex_match_word('criame', x) or regex_match_word('cultivo', x)
            or regex_match_word('criatorio', x) or regex_match_word('acude', x)
            or regex_match_word('gado', x) or regex_match_word('sitio', x)
            or regex_match_word('fumo', x) or regex_match_word('estufa', x)
            or re.search(r'\bcult(ura)? de\b', description(x), flags=re.I)
            or re.search(r'\bcul(llt|l|it)?ivo\b', description(x), flags=re.I)
            or re.search(r'\bboi[s]?\b', description(x), flags=re.I)
            or re.search(r'\bvaca[s]?\b', description(x), flags=re.I)
            or re.search(r'\bsuino[s]?\b', description(x), flags=re.I)
            or re.search(r'\bporco[s]?\b', description(x), flags=re.I)
            or re.search(r'\babelha[s]?\b', description(x), flags=re.I)
            or re.search(r'\b[b]?ovin[oa][s]?\b', description(x), flags=re.I)
            or re.search(r'\bpeixe[s]?\b', description(x), flags=re.I)
            or re.search(r'\bbode[s]?\b', description(x), flags=re.I)
            or re.search(r'\bcabra[s]?\b', description(x), flags=re.I)
            or re.search(r'\bave[s]?\b', description(x), flags=re.I)
            or re.search(r'\bgalinh(a|eiro)[s]?\b', description(x), flags=re.I)
            or re.search(r'\bcavalo[s]?\b', description(x), flags=re.I)
            or re.search(r'\bcurral[s]?\b', description(x), flags=re.I)
            or re.search(r'\bgranja[s]?\b', description(x), flags=re.I)
            or re.search(r'\b(ch|x)iqueiro[s]?\b', description(x), flags=re.I)
            or re.search(r'[a-z]+cultura\b', description(x), flags=re.I)
            or match_any_item_in_list(keywords, x) or aviamentos_urban_rural(x, RURAL_LABEL)
            or cnefe_landuse_ids.farming_establishment == int(x.landuse_id)):
        return poi_labels.scheme.farming
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def farming_id(x):
    if cnefe_landuse_ids.farming_establishment == int(x.landuse_id):
        return poi_labels.scheme.farming
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def farming_word_dist(x):
    keywords = ['fazenda', 'plantio', 'plantacao', 'pecuaria', 'agricola', 'criacao', 'criame', 'acude', 'fumo',
                'sitio', 'corte', 'curral', 'ovelha', 'aviario', 'galpao', 'granja', 'cultivo', 'criatorio', 'gado',
                'estufa', 'cultura', 'cultivo', 'boi', 'vaca', 'suino', 'porco', 'abelha', 'ovino', 'peixe', 'bode',
                'cabra', 'aves', 'galinha', 'galinheiro', 'chiqueiro', 'cavalo', 'egua', 'curral']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.farming
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def farming_sound_dist(x):
    keywords = ['fazenda', 'plantio', 'plantacao', 'pecuaria', 'agricola', 'criacao', 'criame', 'acude', 'fumo',
                'sitio', 'corte', 'curral', 'ovelha', 'aviario', 'galpao', 'granja', 'cultivo', 'criatorio', 'gado',
                'estufa', 'cultura', 'cultivo', 'boi', 'vaca', 'suino', 'porco', 'abelha', 'ovino', 'peixe', 'bode',
                'cabra', 'aves', 'galinha', 'galinheiro', 'chiqueiro', 'cavalo', 'egua', 'curral']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.farming
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def extractive_industries_keywords(x):
    keywords = ['extracao de', 'marmore', 'garimpo', 'mineracao', 'metais preciosos',
                'manganes', 'titanio', 'niobio', 'aluminio', 'moedora de']
    if (re.search(r'\bmine(i)?radora\b', description(x), flags=re.I)
            or regex_match_word('carvao', x) or regex_match_word('minerio', x)
            or regex_match_word('cobre', x) or regex_match_word('estanho', x)
            or regex_match_word('areia', x) or regex_match_word('argila', x)
            or match_any_item_in_list(keywords, x)):
        return poi_labels.scheme.extractive_industries
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def extractive_industries_word_dist(x):
    keywords = ['extracao', 'marmore', 'garimpo', 'mineracao', 'metais', 'metais',
                'manganes', 'titanio', 'niobio', 'aluminio', 'mineradora', 'carvao',
                'minerio', 'cobre', 'estanho', 'argila', 'areia', 'moedora']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.extractive_industries
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def extractive_industries_sound_dist(x):
    keywords = ['extracao', 'marmore', 'garimpo', 'mineracao', 'metais', 'metais',
                'manganes', 'titanio', 'niobio', 'aluminio', 'mineradora', 'carvao',
                'minerio', 'cobre', 'estanho', 'argila', 'areia', 'moedora']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.extractive_industries
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def extractive_industries_industria_keyword(x):
    keywords = ['industria']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.extractive_industries
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def manufacturing_industries_keywords(x):
    keywords = ['abatedouro', 'frigorifico', 'abatedor', 'fabrica', 'confeccoes', 'ferreir', 'textil', 'malharia',
                'metalurgi', 'sederurgi', 'beneficiadora', 'beneficiamento', 'maquinario', 'marcenaria', 'carpintaria',
                'marceneiro', 'carpinteiro', 'estamparia', 'ferreiro']
    if (regex_match_word('abate', x) or match_any_item_in_list(keywords, x)
            or re.search(r'\bconfec(c)?a[o0]\b', description(x), flags=re.I)
            or re.search(r'\bbarca(c|ss)a\b', description(x), flags=re.I)
            or re.search(r'\bindustria\b', description(x), flags=re.I)):
        return poi_labels.scheme.manufacturing_industries
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def manufacturing_industries_empresa_keyword(x):
    if regex_match_word('empresa', x):
        return poi_labels.scheme.manufacturing_industries
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def manufacturing_industries_word_dist(x):
    keywords = ['abatedouro', 'frigorifico', 'abatedor', 'fabrica', 'confeccoes', 'abate', 'confeccao', 'barcassa',
                'carpintaria',
                'barcaca', 'ferreiro', 'metalurgia', 'sederurgia', 'beneficiadora', 'beneficiamento', 'industria',
                'marcenaria',
                'marceneiro', 'carpinteiro', 'textil', 'malharia']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.manufacturing_industries
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def manufacturing_industries_sound_dist(x):
    keywords = ['abatedouro', 'frigorifico', 'abatedor', 'fabrica', 'confeccoes', 'abate', 'confeccao', 'barcassa',
                'carpintaria',
                'barcaca', 'ferreiro', 'metalurgia', 'sederurgia', 'beneficiadora', 'beneficiamento', 'industria',
                'marcenaria',
                'marceneiro', 'carpinteiro', 'textil', 'malharia']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
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
            or re.search(r'\bga[sz]\b', description(x), flags=re.I)
            or re.search(r'\bsub\s?estacao\b', description(x), flags=re.I)):
        return poi_labels.scheme.gas_and_electricity
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def gas_and_electricity_word_dist(x):
    keywords = ['eletricidade', 'energia', 'energetica', 'gas', 'subestacao']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.gas_and_electricity
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def gas_and_electricity_sound_dist(x):
    keywords = ['eletricidade', 'energia', 'energetica', 'gas', 'subestacao']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.gas_and_electricity
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def water_treatment_keywords(x):
    keywords = ['esgoto', 'tratamento de agua', 'departamento de agua', 'estacao de tratamento',
                'distribuidora de agua', 'elevatori', 'saneamento']
    treatment_station_acronyms = ['dmae', 'corsan', 'agespisa', 'caesb', 'aguas guariroba', 'cesama', 'caesa', 'caern',
                                  'casan', 'cagece', 'cagepa', 'caerd', 'cogerh', 'caema', 'deso', 'cosanpa', 'cosampa',
                                  'sanepar', 'cesan', 'cedae', 'compesa', 'sabesp', 'caenf', 'embasa', 'embaza', 'emae',
                                  'sanesul', 'prolagos', 'saneago', 'sanep', 'sanasa']
    if match_any_item_in_list(keywords, x) or regex_match_in_list(treatment_station_acronyms, x):
        return poi_labels.scheme.water_treatment
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def water_treatment_word_dist(x):
    keywords = ['esgoto', 'tratamento', 'departamento', 'estacao', 'elevatorio', 'saneamento']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.water_treatment
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def water_treatment_sound_dist(x):
    keywords = ['esgoto', 'tratamento', 'departamento', 'estacao', 'elevatorio', 'saneamento']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.water_treatment
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def construction_keywords(x):
    keywords = ['incorporadora', 'construcoes', 'incorporacao', 'empreiteira', 'terraplanagem',
                'instalacao hidraulica', 'instalacao eletrica', 'construtora']
    if ((regex_match_word('construcao', x)
         and not regex_match_in_list(['casa', 'em'], x) and not match_any_item_in_list(['mat', 'de construcao'], x))
            or match_any_item_in_list(keywords, x)):
        return poi_labels.scheme.construction
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def construction_word(x):
    if regex_match_word('construcao', x):
        return poi_labels.scheme.construction
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def construction_word_dist(x):
    keywords = ['incorporadora', 'construcoes', 'incorporacao', 'empreiteira', 'terraplanagem',
                'instalacao', 'hidraulica', 'eletrica']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.construction
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def construction_sound_dist(x):
    keywords = ['incorporadora', 'construcoes', 'incorporacao', 'empreiteira', 'terraplanagem',
                'instalacao', 'hidraulica', 'eletrica']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.construction
    else:
        return poi_labels.scheme.undefined


retail_keywords = ['comercio', 'varej', 'venda', 'loja', 'estabelecimento comercial', 'estabelecimentos comerciais',
                   'sala comercial', 'salas comerciais', 'center', 'shopping', 'shoping', 'conjunto comercial',
                   'galeria']


@labeling_function()
def retail_keyword(x):
    if match_any_item_in_list(retail_keywords, x):
        return poi_labels.scheme.retail
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def motor_vehicle_repair_and_retail_keywords(x):
    places = ['oficina', '0ficina', '0fissina', 'ofissina', 'mecanica', 'ferragem', 'borracha']
    keywords = ['martelinho de ouro', 'automotivo', 'motor', 'veiculo', 'concessionaria', 'motores', 'bicicletas']
    if (match_any_item_in_list(places, x) or match_any_item_in_list(keywords, x) or regex_match_word('pecas', x)
            or re.search(r'\bpneu[s]?\b', description(x), flags=re.I)
            or re.search(r'\brodas[s]?\b', description(x), flags=re.I)
            or re.search(r'\bmoto[s]?\b', description(x), flags=re.I)
            or re.search(r'\bmolas\b', description(x), flags=re.I)
            or re.search(r'\bescapamentos?\b', description(x), flags=re.I)
            or re.search(r'\bcarros?\b', description(x), flags=re.I)
            or re.search(r'\bauto[s]?\b', description(x), flags=re.I)
            or re.search(r'\bfun[ei]laria[s]?\b', description(x), flags=re.I)):
        return poi_labels.scheme.motor_vehicle_repair_and_retail
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def motor_vehicle_repair_and_retail_word_dist(x):
    keywords = ['oficina', 'mecanica', 'ferragem', 'pneu', 'roda', 'funilaria', 'motores', 'bicicletas',
                'martelinho', 'automotivo', 'motor', 'veiculo', 'borracharia', 'concessionaria', 'escapamentos']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.motor_vehicle_repair_and_retail
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def motor_vehicle_repair_and_retail_sound_dist(x):
    keywords = ['oficina', 'mecanica', 'ferragem', 'pneu', 'roda', 'funilaria', 'motores', 'bicicletar',
                'martelinho', 'automotivo', 'motor', 'veiculo', 'borracharia', 'concessionaria', 'escapamentos']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.motor_vehicle_repair_and_retail
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def wholesale_trade_keyword(x):
    if match_any_item_in_list(['atacado', 'representante', 'distribuidora'], x):
        return poi_labels.scheme.wholesale_trade_except_motor_vehicles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def wholesale_word_dist(x):
    keywords = ['atacado']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.wholesale_trade_except_motor_vehicles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def wholesale_sound_dist(x):
    keywords = ['atacado']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.wholesale_trade_except_motor_vehicles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def non_specialized_retail_trade_keyword(x):
    if (match_all_items(['loja', 'departamento'], x)
            or 'variedade' in description(x)
            or 'utilidade' in description(x)):
        return poi_labels.scheme.non_specialized_retail_trade
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def non_specialized_retail_trade_word_dist(x):
    keywords = ['variedade', 'utilidade', 'departamentos']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.non_specialized_retail_trade
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def non_specialized_retail_trade_sound_dist(x):
    keywords = ['variedade', 'utilidade', 'departamentos']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
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
def non_specialized_retail_foodstuffs_supermarkets_word_dist(x):
    keywords = ['supermercado', 'mercadao', 'hipermercado']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.non_specialized_retail_foodstuffs_supermarkets
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def non_specialized_retail_foodstuffs_supermarkets_sound_dist(x):
    keywords = ['supermercado', 'mercadao', 'hipermercado']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.non_specialized_retail_foodstuffs_supermarkets
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def non_specialized_retail_foodstuffs_grocery_stores_keyword(x):
    keywords = ['mercearia', 'mercantil']
    armazem = ['armazem', 'amarzem']
    if (match_any_item_in_list(keywords, x)
            or (match_any_item_in_list(armazem, x) and not regex_match_in_list(['de', 'logistica', 'deposito'], x))
            or re.search(r'\b(min[ie]\s?)?mercado', description(x), flags=re.I)):
        return poi_labels.scheme.non_specialized_retail_foodstuffs_grocery_stores
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def non_specialized_retail_foodstuffs_grocery_stores_word_dist(x):
    keywords = ['mercearia', 'armazem', 'minimercado', 'mercado', 'amarzem']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.non_specialized_retail_foodstuffs_grocery_stores
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def non_specialized_retail_foodstuffs_grocery_stores_sound_dist(x):
    keywords = ['mercearia', 'armazem', 'minimercado', 'mercado', 'amarzem']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.non_specialized_retail_foodstuffs_grocery_stores
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_food_beverages_tobacco_keyword(x):
    keywords = ['padaria', 'panificadora', 'casa de carne', 'tabacaria', 'bebidas', 'comercio alimenticio']
    if (match_any_item_in_list(keywords, x) or match_all_items(['distribuidora', 'bebidas'], x)
            or re.search(r'\bconfe(i)?taria\b', description(x), flags=re.I)
            or re.search(r'\bpe(i)?xaria\b', description(x), flags=re.I)
            or re.search(r'\bac(o)?ugue\b', description(x), flags=re.I)):
        return poi_labels.scheme.retail_food_beverages_tobacco
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_food_beverages_tobacco_word_dist(x):
    keywords = ['padaria', 'tabacaria', 'bebidas', 'confeitaria', 'peixaria', 'acougue']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.retail_food_beverages_tobacco
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_food_beverages_tobacco_sound_dist(x):
    keywords = ['padaria', 'tabacaria', 'bebidas', 'confeitaria', 'peixaria', 'acougue']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.retail_food_beverages_tobacco
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_fuel_keyword(x):
    keywords = ['gasolina', 'ipiranga', 'auto posto', 'texaco', 'diesel']
    if (match_any_item_in_list(keywords, x) or regex_match_word('br', x) or regex_match_word('shell', x)
            or re.search(r'\bcombustive(l|is)\b', description(x), flags=re.I)):
        return poi_labels.scheme.retail_fuel
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_fuel_word_dist(x):
    keywords = ['gasolina', 'ipiranga', 'auto', 'posto', 'texaco', 'diesel', 'combustivel']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.retail_fuel
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_fuel_sound_dist(x):
    keywords = ['gasolina', 'ipiranga', 'auto', 'posto', 'texaco', 'diesel', 'combustivel']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.retail_fuel
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_building_material_keyword(x):
    keywords = ['vidracaria', 'telhas', 'telhados', 'piscinas']
    if (match_any_item_in_list(keywords, x)
            or re.search(r'\bmat(eria(l|is))?\.? de con(s)?trucao\b', description(x), flags=re.I)):
        return poi_labels.scheme.retail_building_material
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_building_material_word_dist(x):
    keywords = ['vidracaria', 'telhas', 'telhados']
    if (dists.has_any_similar_char_seq(keywords, description(x))
            or (dists.has_any_similar_phonetic_word(['material'], description(x)) or
                dists.has_any_similar_phonetic_word(['materiais'], description(x)))
            and dists.has_any_similar_phonetic_word(['construcao'], description(x))):
        return poi_labels.scheme.retail_building_material
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_computer_communication_household_equipment_keyword(x):
    keywords = ['armarinho', 'mesa e banho', 'eletrodomesticos', 'moveis', 'computador', 'celular', 'cartucho',
                'colchoes', 'colchao', 'tecidos']
    if (match_any_item_in_list(keywords, x)
            or (match_any_item_in_list(['enxovais', 'enxoval'], x) and not match_any_item_in_list(['bebe'], x))):
        return poi_labels.scheme.retail_computer_communication_household_equipment
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_computer_communication_household_equipment_word_dist(x):
    keywords = ['armarinho', 'eletrodomesticos', 'eletro', 'domesticos', 'moveis', 'computador', 'cartucho', 'colchoes',
                'colchao']
    if (dists.has_any_similar_char_seq(keywords, description(x))
            or dists.has_any_similar_char_seq(['mesa'], description(x))
            and dists.has_any_similar_char_seq(['banho'], description(x))):
        return poi_labels.scheme.retail_computer_communication_household_equipment
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_computer_communication_household_equipment_sound_dist(x):
    keywords = ['armarinho', 'eletrodomesticos', 'eletro', 'colchoes', 'colchao',
                'domesticos', 'moveis', 'computador', 'cartucho']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
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
def retail_sport_culture_recreation_articles_word_dist(x):
    if (dists.has_any_similar_char_seq(['livraria', 'papelaria'], description(x))
            or 'loja' in description(x)
            and dists.has_any_similar_char_seq(['esportes', 'brinquedo'], description(x))):
        return poi_labels.scheme.retail_sport_culture_recreation_articles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_sport_culture_recreation_articles_sound_dist(x):
    keywords = ['livraria', 'papelaria', 'loja de esportes', 'loja de brinquedo']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.retail_sport_culture_recreation_articles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_keyword(x):
    keywords = ['boticario', 'cosmetico', 'farmacia', 'drogaria', 'oculos', 'otica', 'ortopedico', 'perfume',
                'perfumaria']
    if (match_any_item_in_list(keywords, x) or re.search(r'\bo(p)?tic[a0o]\b', description(x), flags=re.I)
            or (match_any_item_in_list(['droga', 'farma', 'pharma'], x)
                and not match_any_item_in_list(['distribuidora', 'industria'], x))
            or (match_any_item_in_list(['veterinari'], x)
                and match_any_item_in_list(['produto'], x))):
        return poi_labels.scheme.retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_word_dist(x):
    keywords = ['boticario', 'cosmetico', 'farmacia', 'drogaria', 'oculos', 'otica', 'ortopedico', 'perfume',
                'perfumaria']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_sound_dist(x):
    keywords = ['boticario', 'cosmetico', 'farmacia', 'drogaria', 'oculos', 'otica', 'ortopedico', 'perfume',
                'perfumaria']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.retail_sport_culture_recreation_articles
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_new_products_non_specified_previously_and_second_hand_keyword(x):
    keywords = ['noiva', 'roupas intimas', 'bijoux', 'fashion', 'presentes', 'calcados', 'bazar', 'jeans', 'vestuario',
                'brecho', 'loja de relogios', 'joalheria', 'floricultura', 'antiquario', 'antiguidades', 'emporio',
                'estabelecimento comercial', 'presentes', 'usado', 'shop', 'artesanato', 'camisaria', 'hair',
                'magazine']
    if (match_any_item_in_list(keywords, x) or match_any_item_in_list(retail_keywords, x)
            or aviamentos_urban_rural(x, URBAN_LABEL)
            or (match_any_item_in_list(['enxovais', 'enxoval'], x) and match_any_item_in_list(['bebe'], x))
            or re.search(r'\bro(u|p|up)a(s)?\b', description(x), flags=re.I)
            or re.search(r'\bmalha(s)?\b', description(x), flags=re.I)
            or re.search(r'\bmoda(s)?\b', description(x), flags=re.I)
            or re.search(r'\bl[iae]ngerie\b', description(x), flags=re.I)
            or re.search(r'\bpet\s?shop\b', description(x), flags=re.I)
            or re.search(r'\bbij(o|u|ou)teria\b', description(x), flags=re.I)):
        return poi_labels.scheme.retail_new_products_non_specified_previously_and_second_hand
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_new_products_non_specified_previously_and_second_hand_word_dist(x):
    keywords = ['roupas', 'malhas', 'modas', 'lingerie', 'bijuteria', 'intimas', 'bijoux', 'fashion', 'presentes',
                'calcados', 'bazar', 'jeans', 'vestuario', 'brecho', 'relogios', 'joalheria', 'floricultura',
                'antiquario', 'antiguidades', 'emporio', 'presentes', 'magazine']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.retail_new_products_non_specified_previously_and_second_hand
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def retail_new_products_non_specified_previously_and_second_hand_sound_dist(x):
    keywords = ['roupas', 'malhas', 'modas', 'lingerie', 'bijuteria', 'intimas', 'bijoux', 'fashion', 'presentes',
                'calcados', 'bazar', 'jeans', 'vestuario', 'brecho', 'relogios', 'joalheria', 'floricultura',
                'antiquario', 'antiguidades', 'emporio', 'presentes', 'magazine']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.retail_new_products_non_specified_previously_and_second_hand
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def transport_warehousing_mail_keywords(x):
    keywords = ['transporte']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.transport_warehousing_mail
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def ground_transportation_keywords(x):
    keywords = ['estacao de trem', 'estacao de metro', 'estacao rodoviaria', 'teleferico', 'moto taxi', 'mototaxi',
                'onibus']
    if match_any_item_in_list(keywords, x) or regex_match_word('taxi', x):
        return poi_labels.scheme.ground_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def ground_transportation_word_dist(x):
    keywords = ['trem', 'metro', 'rodoviaria', 'teleferico', 'taxi', 'mototaxi', 'onibus']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.ground_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def ground_transportation_sound_dist(x):
    keywords = ['trem', 'metro', 'rodoviaria', 'teleferico', 'taxi', 'mototaxi', 'onibus']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.ground_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def water_transportation_keywords(x):
    keywords = ['catamara']
    if (match_any_item_in_list(keywords, x) or regex_match_word('balsa', x)
            or re.search(r'\bbarc[oa]\b', description(x), flags=re.I)):
        return poi_labels.scheme.water_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def water_transportation_word_dist(x):
    keywords = ['catamara', 'barco', 'balsa']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.water_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def water_transportation_sound_dist(x):
    keywords = ['catamara', 'barco', 'balsa']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
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
def air_transportation_word_dist(x):
    keywords = ['aeroporto']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.air_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def air_transportation_sound_dist(x):
    keywords = ['catamara', 'barco', 'balsa']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.air_transportation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def storage_auxiliary_transport_activities_keywords(x):
    keywords = ['estacionamento', 'galpao', 'paiol', 'tulha', 'tuia', 'tulia', 'deposito', 'logistica', 'armazena',
                'armazem de', 'amarzem de', 'armarsem de', 'garagem']
    if match_any_item_in_list(keywords, x):
        return poi_labels.scheme.storage_auxiliary_transport_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def storage_auxiliary_transport_activities_word_dist(x):
    keywords = ['estacionamento', 'galpao', 'paiol', 'tulha', 'deposito', 'logistica', 'armazenagem', 'armazenamento',
                'garagem']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.storage_auxiliary_transport_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def storage_auxiliary_transport_activities_sound_dist(x):
    keywords = ['estacionamento', 'galpao', 'paiol', 'tulha', 'deposito', 'logistica', 'armazenagem', 'armazenamento',
                'garagem']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
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
def mail_and_other_delivery_services_word_dist(x):
    keywords = ['correio', 'fedex', 'sedex']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.mail_and_other_delivery_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def mail_and_other_delivery_services_sound_dist(x):
    keywords = ['correio', 'fedex', 'sedex']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
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
def accommodation_word_dist(x):
    keywords = ['hotel', 'pousada', 'hospedaria', 'hospedagem']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.accommodation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def accommodation_sound_dist(x):
    keywords = ['hotel', 'pousada', 'hospedaria', 'hospedagem']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.accommodation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def eating_places_keywords(x):
    common_foods = ['pizza', 'hamburgue', 'sushi', 'pastel', 'pasteis', 'sorvete', 'churras', 'bebidas', 'beer',
                    'burger',
                    'bauru', 'acaraje', 'vitamina', 'batida', 'salgado', 'salgadinho', 'galeto', 'esfiha']
    common_places = ['lanche', 'lanchonete', 'boteco', 'cafeteria', 'restaurante', 'buffet', 'espetinho', 'grill',
                     'vitaminosa', 'espeto', 'galeteria', 'barzinho']
    if (regex_match_word('bar', x) or regex_match_word('acai', x) or regex_match_word('massa(s)?', x)
            or re.search(r'\bdoce(s)?\b', description(x), flags=re.I)
            or match_any_item_in_list(common_places, x) or match_any_item_in_list(common_foods, x)):
        return poi_labels.scheme.eating_places
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def eating_places_word_dist(x):
    keywords = ['pizza', 'pizzaria', 'hamburguer', 'hamburgueria', 'burger', 'sushi', 'pastel', 'pastelaria', 'pasteis',
                'barzinho',
                'sorvete', 'sorveteria', 'churrasco', 'churrascaria', 'doces', 'bebidas', 'galeto', 'galeteria',
                'vitaminosa',
                'lanche', 'lancheria', 'lanchonete', 'boteco', 'cafeteria', 'restaurante', 'buffet', 'espetinho',
                'esfiha']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.eating_places
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def eating_places_sound_dist(x):
    keywords = ['pizza', 'pizzaria', 'hamburguer', 'hamburgueria', 'burger', 'sushi', 'pastel', 'pastelaria', 'pasteis',
                'barzinho',
                'sorvete', 'sorveteria', 'churrasco', 'churrascaria', 'doces', 'bebidas', 'galeto', 'galeteria',
                'vitaminosa',
                'lanche', 'lancheria', 'lanchonete', 'boteco', 'cafeteria', 'restaurante', 'buffet', 'espetinho',
                'esfiha']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.eating_places
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def information_and_communication_keywords(x):
    keywords = ['software', 'estudio', 'informatica', 'computacao', 'informacao', 'internet', 'midia', 'video',
                'televisao', 'revista', 'jornal', 'jornais', 'news', 'radio', 'chaveiro']
    internet_providers = ['oi', 'tim', 'net', 'claro', 'vivo', 'gvt', 'embratel']
    if (regex_match_in_list(['grafica', 'tv', 'fm', 'am'], x)
            or re.search(r'\blan\s?h[ao]use\b', description(x), flags=re.I)
            or match_any_item_in_list(keywords, x) or regex_match_in_list(internet_providers, x)):
        return poi_labels.scheme.information_and_communication
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def information_and_communication_word_dist(x):
    keywords = ['software', 'estudio', 'informatica', 'lanhouse', 'grafica', 'copias', 'computacao', 'informacao',
                'midia', 'televisao', 'revista', 'jornal', 'video']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.information_and_communication
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def information_and_communication_sound_dist(x):
    keywords = ['software', 'estudio', 'informatica', 'lanhouse', 'grafica', 'copias', 'computacao', 'informacao',
                'midia', 'televisao', 'revista', 'jornal', 'video']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.information_and_communication
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def financial_activities_insurance_keywords(x):
    keywords = ['banco', 'seguro', 'financeiro', 'financiamento']
    banks = ['santander', 'bradesco', 'banco do brasil', 'itau', 'caixa', 'banrisul']
    if match_any_item_in_list(keywords, x) or regex_match_in_list(banks, x):
        return poi_labels.scheme.financial_activities_insurance
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def financial_activities_insurance_word_dist(x):
    keywords = ['banco', 'seguro', 'financeiro', 'financiamento']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.financial_activities_insurance
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def financial_activities_insurance_sound_dist(x):
    keywords = ['banco', 'seguro', 'financeiro', 'financiamento']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.financial_activities_insurance
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def real_estate_activities_keywords(x):
    if re.search(r'\bimobiliari[ao0]\b', description(x), flags=re.I):
        return poi_labels.scheme.real_estate_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def real_estate_activities_word_dist(x):
    keywords = ['imobiliaria']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.real_estate_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def real_estate_activities_sound_dist(x):
    keywords = ['imobiliaria']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.real_estate_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def professional_scientific_and_technic_activities_keywords(x):
    keywords = ['cartorio', 'tabeliao', 'tabelionato', 'registro civil', 'juizado', 'escritorio', 'adestra'
                                                                                                  'consultoria',
                'oficio de notas', 'despachante', 'escritorio de', 'advocacia', 'publici', 'propaganda',
                'advogad', 'contador', 'contab', 'arquitet', 'engenh', 'publici', 'pronto vet', 'prontovet']
    if (match_any_item_in_list(keywords, x)
            or (match_any_item_in_list(['veterinari', 'agovet'], x) and not match_any_item_in_list(['produto'], x))):
        return poi_labels.scheme.professional_scientific_and_technic_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def professional_scientific_and_technic_activities_word_dist(x):
    keywords = ['cartorio', 'tabeliao', 'tabelionato', 'registro', 'juizado', 'escritorio', 'consultoria', 'adestrador',
                'despachante', 'advocacia', 'advogado', 'contador', 'contabilidade', 'contaveis', 'arquiteto',
                'adestramento',
                'arqiutetura', 'engenharia', 'engenheiro', 'veterinaria', 'publicidade', 'publicitario']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.professional_scientific_and_technic_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def professional_scientific_and_technic_activities_sound_dist(x):
    keywords = ['cartorio', 'tabeliao', 'tabelionato', 'registro', 'juizado', 'escritorio', 'consultoria',
                'despachante', 'advocacia', 'advogado', 'contador', 'contabilidade', 'contaveis', 'arquiteto',
                'arqiutetura', 'engenharia', 'engenheiro', 'veterinaria', 'publicidade', 'publicitario']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.professional_scientific_and_technic_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def administrative_activities_complementary_services_keywords(x):
    keywords = ['loteria', 'loterica', 'aluguel de carro', 'locadora', 'locacao de automove', 'turismo',
                'aluguel', 'alugueis', 'festas']
    if match_any_item_in_list(keywords, x) or re.search(r'(agencia)? (de)? via[gj]e(m|ns)', description(x), flags=re.I):
        return poi_labels.scheme.administrative_activities_complementary_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def administrative_activities_complementary_services_word_dist(x):
    keywords = ['loteria', 'loterica', 'aluguel', 'locacao', 'locadora', 'turismo']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.administrative_activities_complementary_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def administrative_activities_complementary_services_sound_dist(x):
    keywords = ['loteria', 'loterica', 'aluguel', 'locacao', 'locadora', 'turismo']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.administrative_activities_complementary_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def public_administration_social_security_defence_keywords(x):
    keywords = ['prefeitura', 'delegacia', 'batalhao', 'centro administrativo', 'militar', 'policia', 'vara civel',
                'civil']
    if match_any_item_in_list(keywords, x) or regex_match_in_list(['dp', 'bpm', 'detran', 'contran', 'ciretran'], x):
        return poi_labels.scheme.public_administration_social_security_defence
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def public_administration_social_security_defence_word_dist(x):
    keywords = ['prefeitura', 'delegacia', 'batalhao', 'administrativo', 'militar', 'policia', 'civel', 'civil']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.public_administration_social_security_defence
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def public_administration_social_security_defence_sound_dist(x):
    keywords = ['prefeitura', 'delegacia', 'batalhao', 'administrativo', 'militar', 'policia', 'civel', 'civil']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
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
    if 'educacao' in description(x:
        return poi_labels.scheme.education
    else:
        return poi_labels.scheme.undefined
"""


@labeling_function()
def education_keywords(x):
    keywords = ['escola', 'colegio', 'faculdade', 'universidade', 'creche', 'ensino', 'formacao',
                'formacao de condutores', 'educacao infantil', 'bercario', 'alfabetiza', 'escolinha']
    if (match_any_item_in_list(keywords, x) or regex_match_word('cfc', x) or regex_match_word('cmei', x)
            or cnefe_landuse_ids.educational_establishment == int(x.landuse_id)):
        return poi_labels.scheme.education
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def education_word_dist(x):
    keywords = ['escola', 'colegio', 'faculdade', 'universidade', 'creche', 'ensino', 'formacao',
                'condutores', 'bercario', 'alfabetiza', 'escolinha']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.education
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def education_sound_dist(x):
    keywords = ['escola', 'colegio', 'faculdade', 'universidade', 'creche', 'ensino', 'formacao',
                'condutores', 'bercario', 'alfabetiza', 'escolinha']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.education
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def education_id(x):
    if cnefe_landuse_ids.educational_establishment == int(x.landuse_id):
        return poi_labels.scheme.education
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def human_health_social_services_keywords(x):
    keywords = ['consultorio', 'cardiologista', 'dentista', 'odonto', 'psicolog', 'fisioterap', 'terapia', 'dermatolog',
                'diagnostico', 'ambulatori',
                'pronto socorro', 'hospital', 'hospicio', 'medic', 'de assistencia', 'oftalmo', 'laboratorio']
    if (match_any_item_in_list(keywords, x)
            or cnefe_landuse_ids.health_establishment == int(x.landuse_id)):
        return poi_labels.scheme.human_health_social_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def human_health_social_services_word_dist(x):
    keywords = ['consultorio', 'cardiologista', 'dentista', 'odontologista', 'odontologico', 'odontologia',
                'psicologia', 'psicologo', 'fisioterapia', 'fisioterapeuta', 'terapia', 'diagnostico',
                'socorro', 'hospital', 'hospicio', 'medico', 'laboratorio']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.human_health_social_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def human_health_social_services_sound_dist(x):
    keywords = ['consultorio', 'cardiologista', 'dentista', 'odontologista', 'odontologico', 'odontologia',
                'psicologia', 'psicologo', 'fisioterapia', 'fisioterapeuta', 'terapia', 'diagnostico',
                'socorro', 'hospital', 'hospicio', 'medico', 'laboratorio']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.human_health_social_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def human_health_id(x):
    if cnefe_landuse_ids.health_establishment == int(x.landuse_id):
        return poi_labels.scheme.human_health_social_services
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def arts_culture_sport_recreation_keywords(x):
    keywords = ['teatro', 'galeria de arte', 'cinema', 'museu', 'biblioteca', 'clube social', 'cassino',
                'academia', 'esporte', 'jogo', 'lazer', 'bicicletaria', 'bike', 'zoologico',
                'complexo esportivo', 'ginasio', 'esportivo', 'brinquedoteca', 'musica']
    if match_any_item_in_list(keywords, x) or regex_match_in_list(['praca', 'parque'], x):
        return poi_labels.scheme.arts_culture_sport_recreation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def arts_culture_sport_recreation_word_dist(x):
    keywords = ['teatro', 'cinema', 'museu', 'biblioteca', 'clube', 'praca', 'parque', 'social', 'cassino', 'academia',
                'esporte', 'ginasio', 'esportivo', 'brinquedoteca', 'bicicletaria', 'zoologico']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.arts_culture_sport_recreation
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def arts_culture_sport_recreation_sound_dist(x):
    keywords = ['teatro', 'cinema', 'museu', 'biblioteca', 'clube', 'praca', 'parque', 'social', 'cassino', 'academia',
                'esporte', 'ginasio', 'esportivo', 'brinquedoteca', 'bicicletaria']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
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
def international_organisms_other_extraterritorial_institutions_word_dist(x):
    keywords = ['consulado', 'embaixada']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.international_organisms_other_extraterritorial_institutions
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def international_organisms_other_extraterritorial_institutions_sound_dist(x):
    keywords = ['consulado', 'embaixada']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.international_organisms_other_extraterritorial_institutions
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def other_service_activities_keywords(x):
    keywords = ['cabeleireiro', 'barbearia', 'manicure', 'tatuagem', 'alfaiate', 'unhas', 'biju', 'estetica',
                'empresa de', 'alfaiat', 'relojoeiro', 'barba', 'coiffeur', 'maquiador', 'maquiagem',
                'costureira', 'salao de', 'hotel para ', 'reparo', 'caes', 'gatos', 'animais', 'sindica', 'cabelo',
                'bicicleta', 'lavanderia', 'tosa e banho', 'canil', 'gatil', 'funeraria', 'cemiterio', 'cremacao',
                'sepultamento', 'funeral']
    if (re.search(r'\bcabe[rl]e(i)?[lr]e(i)?r[oa](s)?\b', description(x),
                  flags=re.I)  # cabeleireiro, cabelerero, cabeleleiro, cabelelero
            or re.search(r'\bcabe[rl]e(i)?r[oa](s)?\b', description(x), flags=re.I)  # cabeleiro
            or re.search(r'\bbele[sz]a?\b', description(x), flags=re.I)
            or re.search(r'\bta(t)*oo\b', description(x), flags=re.I)
            or re.search(r'assist(encia)? tec(nica)?', description(x), flags=re.I)
            or re.search(r'foto(s|graf(o|ia|ica))', description(x), flags=re.I)
            or match_any_item_in_list(keywords, x) or regex_match_in_list(["oab", "crea", "crm", "cremers"], x)):
        return poi_labels.scheme.other_service_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def other_service_activities_word_dist(x):
    keywords = ['cabeleireiro', 'barbearia', 'manicure', 'tatuagem', 'tattoo', 'alfaiate', 'beleza', 'petshop',
                'caes', 'costureira', 'fotografo', 'fotografia', 'fotos', 'salao', 'reparo', 'gatos', 'animais',
                'unhas', 'biju', 'estetica', 'cabelo', 'bicicleta', 'maquiador', 'maquiagem', 'funeraria', 'cemiterio',
                'cremacao', 'sepultamento', 'funeral']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.other_service_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def other_service_activities_sound_dist(x):
    keywords = ['cabeleireiro', 'barbearia', 'manicure', 'tatuagem', 'tattoo', 'alfaiate', 'beleza', 'petshop',
                'caes', 'costureira', 'fotografo', 'fotografia', 'fotos', 'salao', 'reparo', 'gatos', 'animais',
                'unhas', 'biju', 'estetica', 'cabelo', 'bicicleta', 'maquiador', 'maquiagem', 'funeraria', 'cemiterio',
                'cremacao', 'sepultamento', 'funeral']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
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
                    or regex_match_word('orixa', x) or regex_match_word('wesleyana', x)
                    or 'nossa senhora' in description(x))
    if (int(x.landuse_id) not in [cnefe_landuse_ids.educational_establishment, cnefe_landuse_ids.health_establishment]
            and ('igreja' in description(x) or 'templo' in description(x)
                 or re.search(r'\bespirit(a|o|ual|ualidade)\b', description(x), flags=re.I)
                 or re.search(r'\bcatolic[oa]\b', description(x), flags=re.I)
                 or re.search(r'\bevangelic[oa]\b', description(x), flags=re.I)
                 or 'umbanda' in description(x) or 'candomble' in description(x)
                 or 'judaica' in description(x) or 'batista' in description(x)
                 or 'capela' in description(x) or 'catedral' in description(x)
                 or 'sinagoga' in description(x) or 'catequetico' in str(
                        x.landuse_description).lower()
                 or 'evangel' in description(x) or has_entities)):
        return poi_labels.scheme.churches_temples_religious_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def churches_temples_religious_activities_word_dist(x):
    keywords = ['deus', 'jesus', 'cristo', 'ogum', 'iemanja', 'exu', 'oxala', 'omulu', 'oxum', 'batista', 'catedral',
                'xango', 'orixa', 'igreja', 'templo', 'espirita', 'espirito', 'espiritual', 'espiritualidade',
                'wesleyana',
                'catolica', 'evangelica', 'umbanda', 'candomble', 'judaica', 'sinagoga', 'capela', 'catequetico']
    if dists.has_any_similar_char_seq(keywords, description(x)):
        return poi_labels.scheme.churches_temples_religious_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def churches_temples_religious_activities_sound_dist(x):
    keywords = ['deus', 'jesus', 'cristo', 'ogum', 'iemanja', 'exu', 'oxala', 'omulu', 'oxum', 'batista', 'catedral',
                'xango', 'orixa', 'igreja', 'templo', 'espirita', 'espirito', 'espiritual', 'espiritualidade',
                'wesleyana',
                'catolica', 'evangelica', 'umbanda', 'candomble', 'judaica', 'sinagoga', 'capela', 'catequetico']
    if dists.has_any_similar_phonetic_word(keywords, description(x)):
        return poi_labels.scheme.churches_temples_religious_activities
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def vacant_keywords(x):
    if (match_any_item_in_list(['baldio', 'inoperante', 'falida', 'falido', 'para alugar', 'alugase'], x)
            or re.search(r'\b(vag|vazi)[oa](s)?\b', description(x), flags=re.I)
            or re.search(r'\bfechad[oa](s)?\b', description(x), flags=re.I)
            or re.search(r'\ba venda\b', description(x), flags=re.I)
            or re.search(r'\bdesocupad[oa](s)?\b', description(x), flags=re.I)
            or re.search(r'\babandonad[oa](s)?\b', description(x), flags=re.I)
            or re.search(r'\bantig[oa]\b', description(x), flags=re.I)):
        return poi_labels.scheme.vacant
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def vacant_dists(x):
    keywords = ['baldio', 'abandonado', 'vago', 'vazio', 'inoperante', 'fechado', 'fechada', 'falido', 'desocupada',
                'abandonada', 'antiga']
    if (dists.has_any_similar_phonetic_word(keywords, description(x))
            or dists.has_any_similar_char_seq(keywords, description(x))):
        return poi_labels.scheme.vacant
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def undefined(x):
    if re.fullmatch(r'[0-9]*', description(x), flags=re.I):
        return poi_labels.scheme.undefined_labeled
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def ongoing_construction(x):
    if match_any_item_in_list(['em construcao', 'casa construcao'], x) \
            or re.fullmatch(r'\bobras?\b', description(x), flags=re.I):
        return poi_labels.scheme.ongoing_construction
    else:
        return poi_labels.scheme.undefined


@labeling_function()
def use_manual_label(x):
    try_last = ["CONSTRUÇÃO", "- COMÉRCIO VAREJISTA", "OBRAS"]
    if str(x.manual_label) == 'nan':
        return poi_labels.scheme.undefined
    else:
        for key in poi_labels.scheme.name_to_label_2way:
            if type(key) is str and str(key) not in try_last:
                if str(key).lower() in str(x.manual_label).lower():
                    return poi_labels.scheme.name_to_label_2way[key]
        for key in try_last:
            if key.lower() in str(x.manual_label).lower():
                return poi_labels.scheme.name_to_label_2way[key]
    return poi_labels.scheme.undefined


def get_lfs_list(word_dists, sound_dists):
    lfs = [
        vacant_keywords,
        use_manual_label,
        human_health_id,
        education_id,
        farming_id,

        farming_keywords,
        extractive_industries_keywords,
        manufacturing_industries_keywords,
        gas_and_electricity_keywords,
        water_treatment_keywords,
        construction_keywords,
        motor_vehicle_repair_and_retail_keywords,
        wholesale_trade_keyword,
        non_specialized_retail_trade_keyword,
        non_specialized_retail_foodstuffs_supermarkets_keyword,
        non_specialized_retail_foodstuffs_grocery_stores_keyword,
        retail_food_beverages_tobacco_keyword,
        retail_fuel_keyword,
        retail_building_material_keyword,
        retail_computer_communication_household_equipment_keyword,
        retail_sport_culture_recreation_articles_keyword,
        retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_keyword,
        retail_new_products_non_specified_previously_and_second_hand_keyword,
        ground_transportation_keywords,
        water_transportation_keywords,
        air_transportation_keywords,
        storage_auxiliary_transport_activities_keywords,
        mail_and_other_delivery_services_keywords,
        transport_warehousing_mail_keywords,
        other_service_activities_keywords,
        accommodation_keywords,
        eating_places_keywords,
        information_and_communication_keywords,
        financial_activities_insurance_keywords,
        real_estate_activities_keywords,
        professional_scientific_and_technic_activities_keywords,
        administrative_activities_complementary_services_keywords,
        public_administration_social_security_defence_keywords,
        education_keywords,
        human_health_social_services_keywords,
        arts_culture_sport_recreation_keywords,
        international_organisms_other_extraterritorial_institutions_keywords,
        churches_temples_religious_activities_keywords,
        manufacturing_industries_empresa_keyword,
        construction_word,
        retail_keyword,
        extractive_industries_industria_keyword,
        undefined
    ]
    if word_dists:
        lfs.append(farming_word_dist)
        lfs.append(extractive_industries_word_dist)
        lfs.append(manufacturing_industries_word_dist)
        lfs.append(gas_and_electricity_word_dist)
        lfs.append(water_treatment_word_dist)
        lfs.append(motor_vehicle_repair_and_retail_word_dist)
        lfs.append(wholesale_word_dist)
        lfs.append(non_specialized_retail_trade_word_dist)
        lfs.append(non_specialized_retail_foodstuffs_supermarkets_word_dist)
        lfs.append(non_specialized_retail_foodstuffs_grocery_stores_word_dist)
        lfs.append(retail_food_beverages_tobacco_word_dist)
        lfs.append(retail_fuel_word_dist)
        lfs.append(retail_building_material_word_dist)
        lfs.append(retail_computer_communication_household_equipment_word_dist)
        lfs.append(retail_sport_culture_recreation_articles_word_dist)
        lfs.append(retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_word_dist)
        lfs.append(retail_new_products_non_specified_previously_and_second_hand_word_dist)
        lfs.append(ground_transportation_word_dist)
        lfs.append(water_transportation_word_dist)
        lfs.append(air_transportation_word_dist)
        lfs.append(storage_auxiliary_transport_activities_word_dist)
        lfs.append(mail_and_other_delivery_services_word_dist)
        lfs.append(accommodation_word_dist)
        lfs.append(eating_places_word_dist)
        lfs.append(information_and_communication_word_dist)
        lfs.append(financial_activities_insurance_word_dist)
        lfs.append(real_estate_activities_word_dist)
        lfs.append(professional_scientific_and_technic_activities_word_dist)
        lfs.append(administrative_activities_complementary_services_word_dist)
        lfs.append(public_administration_social_security_defence_word_dist)
        lfs.append(education_word_dist)
        lfs.append(human_health_social_services_word_dist)
        lfs.append(arts_culture_sport_recreation_word_dist)
        lfs.append(international_organisms_other_extraterritorial_institutions_word_dist)
        lfs.append(other_service_activities_word_dist)
        lfs.append(construction_word_dist)
        lfs.append(churches_temples_religious_activities_word_dist)
    if sound_dists:
        lfs.append(vacant_dists)
        lfs.append(farming_sound_dist)
        lfs.append(extractive_industries_sound_dist)
        lfs.append(manufacturing_industries_sound_dist)
        lfs.append(gas_and_electricity_sound_dist)
        lfs.append(water_treatment_sound_dist)
        lfs.append(motor_vehicle_repair_and_retail_sound_dist)
        lfs.append(wholesale_sound_dist)
        lfs.append(non_specialized_retail_trade_sound_dist)
        lfs.append(non_specialized_retail_foodstuffs_supermarkets_sound_dist)
        lfs.append(non_specialized_retail_foodstuffs_grocery_stores_sound_dist)
        lfs.append(retail_food_beverages_tobacco_sound_dist)
        lfs.append(retail_fuel_sound_dist)
        lfs.append(retail_computer_communication_household_equipment_sound_dist)
        lfs.append(retail_sport_culture_recreation_articles_sound_dist)
        lfs.append(retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_sound_dist)
        lfs.append(retail_new_products_non_specified_previously_and_second_hand_sound_dist)
        lfs.append(ground_transportation_sound_dist)
        lfs.append(water_transportation_sound_dist)
        lfs.append(air_transportation_sound_dist)
        lfs.append(storage_auxiliary_transport_activities_sound_dist)
        lfs.append(mail_and_other_delivery_services_sound_dist)
        lfs.append(accommodation_sound_dist)
        lfs.append(eating_places_sound_dist)
        lfs.append(information_and_communication_sound_dist)
        lfs.append(financial_activities_insurance_sound_dist)
        lfs.append(real_estate_activities_sound_dist)
        lfs.append(professional_scientific_and_technic_activities_sound_dist)
        lfs.append(administrative_activities_complementary_services_sound_dist)
        lfs.append(public_administration_social_security_defence_sound_dist)
        lfs.append(education_sound_dist)
        lfs.append(human_health_social_services_sound_dist)
        lfs.append(arts_culture_sport_recreation_sound_dist)
        lfs.append(international_organisms_other_extraterritorial_institutions_sound_dist)
        lfs.append(other_service_activities_sound_dist)
        lfs.append(construction_sound_dist)
        lfs.append(churches_temples_religious_activities_sound_dist)
    return lfs


all_lfs_list = [
    vacant_keywords,
    use_manual_label,
    human_health_id,
    education_id,
    farming_id,

    farming_keywords,
    extractive_industries_keywords,
    manufacturing_industries_keywords,
    gas_and_electricity_keywords,
    water_treatment_keywords,
    construction_keywords,
    motor_vehicle_repair_and_retail_keywords,
    wholesale_trade_keyword,
    non_specialized_retail_trade_keyword,
    non_specialized_retail_foodstuffs_supermarkets_keyword,
    non_specialized_retail_foodstuffs_grocery_stores_keyword,
    retail_food_beverages_tobacco_keyword,
    retail_fuel_keyword,
    retail_building_material_keyword,
    retail_computer_communication_household_equipment_keyword,
    retail_sport_culture_recreation_articles_keyword,
    retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_keyword,
    retail_new_products_non_specified_previously_and_second_hand_keyword,
    ground_transportation_keywords,
    water_transportation_keywords,
    air_transportation_keywords,
    storage_auxiliary_transport_activities_keywords,
    mail_and_other_delivery_services_keywords,
    other_service_activities_keywords,
    accommodation_keywords,
    eating_places_keywords,
    information_and_communication_keywords,
    financial_activities_insurance_keywords,
    real_estate_activities_keywords,
    professional_scientific_and_technic_activities_keywords,
    administrative_activities_complementary_services_keywords,
    public_administration_social_security_defence_keywords,
    education_keywords,
    human_health_social_services_keywords,
    arts_culture_sport_recreation_keywords,
    international_organisms_other_extraterritorial_institutions_keywords,
    churches_temples_religious_activities_keywords,
    construction_word,
    retail_keyword,
    extractive_industries_industria_keyword,
    undefined,

    farming_sound_dist,
    extractive_industries_sound_dist,
    manufacturing_industries_sound_dist,
    gas_and_electricity_sound_dist,
    water_treatment_sound_dist,
    construction_sound_dist,
    motor_vehicle_repair_and_retail_sound_dist,
    wholesale_sound_dist,
    non_specialized_retail_trade_sound_dist,
    non_specialized_retail_foodstuffs_supermarkets_sound_dist,
    non_specialized_retail_foodstuffs_grocery_stores_sound_dist,
    retail_food_beverages_tobacco_sound_dist,
    retail_fuel_sound_dist,
    retail_computer_communication_household_equipment_sound_dist,
    retail_sport_culture_recreation_articles_sound_dist,
    retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_sound_dist,
    retail_new_products_non_specified_previously_and_second_hand_sound_dist,
    ground_transportation_sound_dist,
    water_transportation_sound_dist,
    air_transportation_sound_dist,
    storage_auxiliary_transport_activities_sound_dist,
    mail_and_other_delivery_services_sound_dist,
    accommodation_sound_dist,
    eating_places_sound_dist,
    information_and_communication_sound_dist,
    financial_activities_insurance_sound_dist,
    real_estate_activities_sound_dist,
    professional_scientific_and_technic_activities_sound_dist,
    administrative_activities_complementary_services_sound_dist,
    public_administration_social_security_defence_sound_dist,
    education_sound_dist,
    human_health_social_services_sound_dist,
    arts_culture_sport_recreation_sound_dist,
    international_organisms_other_extraterritorial_institutions_sound_dist,
    other_service_activities_sound_dist,
    churches_temples_religious_activities_sound_dist,

    farming_word_dist,
    extractive_industries_word_dist,
    manufacturing_industries_word_dist,
    gas_and_electricity_word_dist,
    water_treatment_word_dist,
    construction_word_dist,
    motor_vehicle_repair_and_retail_word_dist,
    wholesale_word_dist,
    non_specialized_retail_trade_word_dist,
    non_specialized_retail_foodstuffs_supermarkets_word_dist,
    non_specialized_retail_foodstuffs_grocery_stores_word_dist,
    retail_food_beverages_tobacco_word_dist,
    retail_fuel_word_dist,
    retail_building_material_word_dist,
    retail_computer_communication_household_equipment_word_dist,
    retail_sport_culture_recreation_articles_word_dist,
    retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles_word_dist,
    retail_new_products_non_specified_previously_and_second_hand_word_dist,
    ground_transportation_word_dist,
    water_transportation_word_dist,
    air_transportation_word_dist,
    storage_auxiliary_transport_activities_word_dist,
    mail_and_other_delivery_services_word_dist,
    accommodation_word_dist,
    eating_places_word_dist,
    information_and_communication_word_dist,
    financial_activities_insurance_word_dist,
    real_estate_activities_word_dist,
    professional_scientific_and_technic_activities_word_dist,
    administrative_activities_complementary_services_word_dist,
    public_administration_social_security_defence_word_dist,
    education_word_dist,
    human_health_social_services_word_dist,
    arts_culture_sport_recreation_word_dist,
    international_organisms_other_extraterritorial_institutions_word_dist,
    other_service_activities_word_dist,
    churches_temples_religious_activities_word_dist
]
