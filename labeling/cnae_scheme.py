"""
ESTRUTURA DETALHADA DA CNAE-SUBCLASSES 2.3

AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQUICULTURA
INDÚSTRIAS EXTRATIVAS
INDÚSTRIAS DE TRANSFORMAÇÃO
ELETRICIDADE E GÁS
ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO
CONSTRUÇÃO
COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS
- COMÉRCIO E REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS
- COMÉRCIO POR ATACADO, EXCETO VEÍCULOS AUTOMOTORES E MOTOCICLETAS
- COMÉRCIO VAREJISTA
- - COMÉRCIO VAREJISTA NÃO ESPECIALIZADO
- - - COMÉRCIO VAREJISTA DE MERCADORIAS EM GERAL, COM PREDOMINÂNCIA DE PRODUTOS ALIMENTÍCIOS - HIPERMERCADOS E SUPERMERCADOS
- - - COMÉRCIO VAREJISTA DE MERCADORIAS EM GERAL, COM PREDOMINÂNCIA DE PRODUTOS ALIMENTÍCIOS - MINIMERCADOS, MERCEARIAS E ARMAZÉNS
- - COMÉRCIO VAREJISTA DE PRODUTOS ALIMENTÍCIOS, BEBIDAS E FUMO
- - COMÉRCIO VAREJISTA DE COMBUSTÍVEIS PARA VEÍCULOS AUTOMOTORES
- - COMÉRCIO VAREJISTA DE MATERIAL DE CONSTRUÇÃO
- - COMÉRCIO VAREJISTA DE EQUIPAMENTOS DE INFORMÁTICA E COMUNICAÇÃO; EQUIPAMENTOS E ARTIGOS DE USO DOMÉSTICO
- - COMÉRCIO VAREJISTA DE ARTIGOS CULTURAIS, RECREATIVOS E ESPORTIVOS
- - COMÉRCIO VAREJISTA DE PRODUTOS FARMACÊUTICOS, PERFUMARIA E COSMÉTICOS E ARTIGOS MÉDICOS, ÓPTICOS E ORTOPÉDICOS
- - COMÉRCIO VAREJISTA DE PRODUTOS NOVOS NÃO ESPECIFICADOS ANTERIORMENTE E DE PRODUTOS USADOS
TRANSPORTE, ARMAZENAGEM E CORREIO
- TRANSPORTE TERRESTRE
- TRANSPORTE AQUAVIÁRIO
- TRANSPORTE AÉREO
- ARMAZENAMENTO E ATIVIDADES AUXILIARES DOS TRANSPORTES
- CORREIO E OUTRAS ATIVIDADES DE ENTREGA
ALOJAMENTO E ALIMENTAÇÃO
- ALOJAMENTO
- ALIMENTAÇÃO
INFORMAÇÃO E COMUNICAÇÃO
ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS
ATIVIDADES IMOBILIÁRIAS
ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS
ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES
ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL
EDUCAÇÃO
SAÚDE HUMANA E SERVIÇOS SOCIAIS
ARTES, CULTURA, ESPORTE E RECREAÇÃO
ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS
OUTRAS ATIVIDADES DE SERVIÇOS
IGREJAS, TEMPLOS E ATIVIDADES RELIGIOSAS
DESOCUPADO
NÃO DEFINIDO
"""


class TwoWayDict(dict):
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self) // 2


class SchemeCNAE:
    def __init__(self):
        self._dict = TwoWayDict()
        self._dict["AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQUICULTURA".encode(encoding='latin-1')] = 1
        self._dict["INDÚSTRIAS EXTRATIVAS".encode(encoding='latin-1')] = 2
        self._dict["INDÚSTRIAS DE TRANSFORMAÇÃO".encode(encoding='latin-1')] = 3

        self._dict["ELETRICIDADE E GÁS".encode(encoding='latin-1')] = 4
        self._dict["ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO".encode(encoding='latin-1')] = 5
        self._dict["CONSTRUÇÃO".encode(encoding='latin-1')] = 6

        self._dict["COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS".encode(encoding='latin-1')] = 7
        self._dict["- COMÉRCIO E REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS".encode(encoding='latin-1')] = 8
        self._dict["- COMÉRCIO POR ATACADO, EXCETO VEÍCULOS AUTOMOTORES E MOTOCICLETAS".encode(encoding='latin-1')] = 9
        self._dict["- COMÉRCIO VAREJISTA".encode(encoding='latin-1')] = 10

        self._dict["- - COMÉRCIO VAREJISTA NÃO ESPECIALIZADO".encode(encoding='latin-1')] = 11
        self._dict[
            "- - - COMÉRCIO VAREJISTA DE MERCADORIAS EM GERAL, COM PREDOMINÂNCIA DE PRODUTOS ALIMENTÍCIOS - HIPERMERCADOS E SUPERMERCADOS".encode(encoding='latin-1')] = 12
        self._dict[
            "- - - COMÉRCIO VAREJISTA DE MERCADORIAS EM GERAL, COM PREDOMINÂNCIA DE PRODUTOS ALIMENTÍCIOS - MINIMERCADOS, MERCEARIAS E ARMAZÉNS".encode(encoding='latin-1')] = 13

        self._dict["- - COMÉRCIO VAREJISTA DE PRODUTOS ALIMENTÍCIOS, BEBIDAS E FUMO".encode(encoding='latin-1')] = 14
        self._dict["- - COMÉRCIO VAREJISTA DE COMBUSTÍVEIS PARA VEÍCULOS AUTOMOTORES".encode(encoding='latin-1')] = 15
        self._dict["- - COMÉRCIO VAREJISTA DE MATERIAL DE CONSTRUÇÃO".encode(encoding='latin-1')] = 16
        self._dict["- - COMÉRCIO VAREJISTA DE EQUIPAMENTOS DE INFORMÁTICA E COMUNICAÇÃO; EQUIPAMENTOS E ARTIGOS DE USO DOMÉSTICO".encode(encoding='latin-1')] = 17
        self._dict["- - COMÉRCIO VAREJISTA DE ARTIGOS CULTURAIS, RECREATIVOS E ESPORTIVOS".encode(encoding='latin-1')] = 18
        self._dict["- - COMÉRCIO VAREJISTA DE PRODUTOS FARMACÊUTICOS, PERFUMARIA E COSMÉTICOS E ARTIGOS MÉDICOS, ÓPTICOS E ORTOPÉDICOS".encode(encoding='latin-1')] = 19
        self._dict["- - COMÉRCIO VAREJISTA DE PRODUTOS NOVOS NÃO ESPECIFICADOS ANTERIORMENTE E DE PRODUTOS USADOS".encode(encoding='latin-1')] = 20

        self._dict["TRANSPORTE, ARMAZENAGEM E CORREIO".encode(encoding='latin-1')] = 21
        self._dict["- TRANSPORTE TERRESTRE".encode(encoding='latin-1')] = 22
        self._dict["- TRANSPORTE AQUAVIÁRIO".encode(encoding='latin-1')] = 23
        self._dict["- TRANSPORTE AÉREO".encode(encoding='latin-1')] = 24
        self._dict["- ARMAZENAMENTO E ATIVIDADES AUXILIARES DOS TRANSPORTES".encode(encoding='latin-1')] = 25
        self._dict["- CORREIO E OUTRAS ATIVIDADES DE ENTREGA".encode(encoding='latin-1')] = 26

        self._dict["ALOJAMENTO E ALIMENTAÇÃO".encode(encoding='latin-1')] = 27
        self._dict["- ALOJAMENTO".encode(encoding='latin-1')] = 28
        self._dict["- ALIMENTAÇÃO".encode(encoding='latin-1')] = 29

        self._dict["INFORMAÇÃO E COMUNICAÇÃO".encode(encoding='latin-1')] = 30
        self._dict["ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS".encode(encoding='latin-1')] = 31
        self._dict["ATIVIDADES IMOBILIÁRIAS".encode(encoding='latin-1')] = 32
        self._dict["ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS".encode(encoding='latin-1')] = 33
        self._dict["ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES".encode(encoding='latin-1')] = 34
        self._dict["ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL".encode(encoding='latin-1')] = 35
        self._dict["EDUCAÇÃO".encode(encoding='latin-1')] = 36
        self._dict["SAÚDE HUMANA E SERVIÇOS SOCIAIS".encode(encoding='latin-1')] = 37
        self._dict["ARTES, CULTURA, ESPORTE E RECREAÇÃO".encode(encoding='latin-1')] = 38
        self._dict["ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS".encode(encoding='latin-1')] = 39
        self._dict["OUTRAS ATIVIDADES DE SERVIÇOS".encode(encoding='latin-1')] = 40
        self._dict["IGREJAS, TEMPLOS E ATIVIDADES RELIGIOSAS".encode(encoding='latin-1')] = 41
        self._dict["DESOCUPADO".encode(encoding='latin-1')] = 42
        self._dict["NÃO DEFINIDO".encode(encoding='latin-1')] = -1

        # Rough translation
        self.farming = 1  # farming_keywords
        self.extractive_industries = 2
        self.manufacturing_industries = 3  # manufacturing_industries_keywords
        self.gas_and_electricity = 4
        self.water_treatment = 5  # water_treatment_keywords
        self.construction = 6
        self.retail_and_motor_vehicle_repair_general = 7  # general_retail_keyword
        self.motor_vehicle_repair_and_retail = 8  # motor_vehicle_repair_and_retail_keywords
        self.wholesale_trade_except_motor_vehicles = 9  # wholesale_trade_keyword
        self.retail = 10
        self.non_specialized_retail_trade = 11
        self.non_specialized_retail_foodstuffs_supermarkets = 12
        self.non_specialized_retail_foodstuffs_grocery_stores = 13
        self.retail_food_beverages_tobacco = 14
        self.retail_fuel = 15
        self.retail_building_material = 16
        self.retail_computer_communication_household_equipment = 17
        self.retail_sport_culture_recreation_articles = 18
        self.retail_pharmaceuticals_perfumery_cosmetics_optical_orthopedic_medical_articles = 19
        self.retail_new_products_non_specified_previously_and_second_hand = 20
        self.transport_warehousing_mail = 21
        self.ground_transportation = 22  # ground_transportation_keywords
        self.water_transportation = 23  # water_transportation_keywords
        self.air_transportation = 24  # air_transportation_keywords
        self.storage_auxiliary_transport_activities = 25  # storage_auxiliary_transport_activities_keywords
        self.mail_and_other_delivery_services = 26  # mail_and_other_delivery_services_keywords
        self.accommodation_and_eating_places = 27
        self.accommodation = 28
        self.eating_places = 29  # eating_places_keywords
        self.information_and_communication = 30
        self.financial_activities_insurance = 31
        self.real_estate_activities = 32
        self.professional_scientific_and_technic_activities = 33
        self.administrative_activities_complementary_services = 34
        self.public_administration_social_security_defence = 35
        self.education = 36  # education_keywords
        self.human_health_social_services = 37
        self.arts_culture_sport_recreation = 38
        self.international_organisms_other_extraterritorial_institutions = 39
        self.other_service_activities = 40
        self.churches_temples_religious_activities = 41  # churches_temples_religious_activities_keywords
        self.vacant = 42  # vacant_keywords
        self.undefined_labeled = 43
        self.undefined = -1

        self.name_to_label_2way = self._dict

    def get_label_with(self, key):
        return self._dict[key]


scheme = SchemeCNAE()
