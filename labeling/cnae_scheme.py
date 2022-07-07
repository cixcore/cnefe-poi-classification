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
        self._dict["AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQUICULTURA"] = 1
        self._dict["INDÚSTRIAS EXTRATIVAS"] = 2
        self._dict["INDÚSTRIAS DE TRANSFORMAÇÃO"] = 3

        self._dict["ELETRICIDADE E GÁS"] = 4
        self._dict["ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO"] = 5
        self._dict["CONSTRUÇÃO"] = 6

        self._dict["COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS"] = 7
        self._dict["COMÉRCIO E REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS"] = 8
        self._dict["COMÉRCIO POR ATACADO, EXCETO VEÍCULOS AUTOMOTORES E MOTOCICLETAS"] = 9
        self._dict["COMÉRCIO VAREJISTA"] = 10

        self._dict["COMÉRCIO VAREJISTA NÃO ESPECIALIZADO"] = 11
        self._dict[
            "COMÉRCIO VAREJISTA DE MERCADORIAS EM GERAL, COM PREDOMINÂNCIA DE PRODUTOS ALIMENTÍCIOS - HIPERMERCADOS E SUPERMERCADOS"] = 12
        self._dict[
            "COMÉRCIO VAREJISTA DE MERCADORIAS EM GERAL, COM PREDOMINÂNCIA DE PRODUTOS ALIMENTÍCIOS - MINIMERCADOS, MERCEARIAS E ARMAZÉNS"] = 13

        self._dict["COMÉRCIO VAREJISTA DE PRODUTOS ALIMENTÍCIOS, BEBIDAS E FUMO"] = 14
        self._dict["COMÉRCIO VAREJISTA DE COMBUSTÍVEIS PARA VEÍCULOS AUTOMOTORES"] = 15
        self._dict["COMÉRCIO VAREJISTA DE MATERIAL DE CONSTRUÇÃO"] = 16
        self._dict["COMÉRCIO VAREJISTA DE EQUIPAMENTOS DE INFORMÁTICA E COMUNICAÇÃO; EQUIPAMENTOS E ARTIGOS DE USO DOMÉSTICO"] = 17
        self._dict["COMÉRCIO VAREJISTA DE ARTIGOS CULTURAIS, RECREATIVOS E ESPORTIVOS"] = 18
        self._dict["COMÉRCIO VAREJISTA DE PRODUTOS FARMACÊUTICOS, PERFUMARIA E COSMÉTICOS E ARTIGOS MÉDICOS, ÓPTICOS E ORTOPÉDICOS"] = 19

        self._dict["TRANSPORTE, ARMAZENAGEM E CORREIO"] = 20
        self._dict["TRANSPORTE TERRESTRE"] = 21
        self._dict["TRANSPORTE AQUAVIÁRIO"] = 22
        self._dict["TRANSPORTE AÉREO"] = 23
        self._dict["ARMAZENAMENTO E ATIVIDADES AUXILIARES DOS TRANSPORTES"] = 24
        self._dict["CORREIO E OUTRAS ATIVIDADES DE ENTREGA"] = 25

        self._dict["ALOJAMENTO E ALIMENTAÇÃO"] = 26
        self._dict["ALOJAMENTO"] = 27
        self._dict["ALIMENTAÇÃO"] = 28

        self._dict["INFORMAÇÃO E COMUNICAÇÃO"] = 29
        self._dict["ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS"] = 30
        self._dict["ATIVIDADES IMOBILIÁRIAS"] = 31
        self._dict["ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES"] = 32
        self._dict["ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL"] = 33
        self._dict["EDUCAÇÃO"] = 34
        self._dict["SAÚDE HUMANA E SERVIÇOS SOCIAIS"] = 35
        self._dict["ARTES, CULTURA, ESPORTE E RECREAÇÃO"] = 36
        self._dict["ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS"] = 37
        self._dict["OUTRAS ATIVIDADES DE SERVIÇOS"] = 38
        self._dict["IGREJAS, TEMPLOS E ATIVIDADES RELIGIOSAS"] = 39
        self._dict["DESOCUPADO"] = 40
        self._dict["NÃO DEFINIDO"] = -1

        # Rough translation
        self.farming = 1  # farming_keywords
        self.extractive_industries = 2
        self.manufacturing_industry = 3
        self.gas_and_electricity = 4
        self.water_treatment = 5
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
        self.transport_warehousing_mail = 20
        self.ground_transportation = 21
        self.water_transportation = 22
        self.air_transportation = 23
        self.storage_auxiliary_transport_activities = 24
        self.mail_and_other_delivery_services = 25
        self.accommodation_and_eating_places = 26
        self.accommodation = 27
        self.eating_places = 28  # eating_places_keywords
        self.information_and_communication = 29
        self.financial_activities_insurance = 30
        self.real_estate_activities = 31
        self.administrative_activities_complementary_services = 32
        self.public_administration_social_security_defence = 33
        self.education = 34  # education_keywords
        self.human_health_social_services = 35
        self.arts_culture_sport_recreation = 36
        self.international_organisms_other_extraterritorial_institutions = 37
        self.other_service_activities = 38
        self.churches_temples_religious_activities = 39  # churches_temples_religious_activities_keywords
        self.vacant = 40  # vacant_keywords
        self.undefined = -1




scheme = SchemeCNAE()
