"""
ESTRUTURA DETALHADA DA CNAE-SUBCLASSES 2.3
2010
"""
import re


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
        self._dict["OBRAS"] = 0
        self._dict["AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQUICULTURA"] = 1
        self._dict["INDÚSTRIAS EXTRATIVAS"] = 2
        self._dict["INDÚSTRIAS DE TRANSFORMAÇÃO"] = 3
        self._dict["ELETRICIDADE E GÁS"] = 4
        self._dict["ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO"] = 5
        self._dict["CONSTRUÇÃO"] = 6

        self._dict["IGREJAS, TEMPLOS E ATIVIDADES RELIGIOSAS"] = 7

        self._dict["- COMÉRCIO E REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS"] = 8
        self._dict["- COMÉRCIO POR ATACADO, EXCETO VEÍCULOS AUTOMOTORES E MOTOCICLETAS"] = 9
        self._dict["- COMÉRCIO VAREJISTA"] = 10
        self._dict["- - COMÉRCIO VAREJISTA NÃO ESPECIALIZADO"] = 11
        self._dict[
            "- - - COMÉRCIO VAREJISTA DE MERCADORIAS EM GERAL, COM PREDOMINÂNCIA DE PRODUTOS ALIMENTÍCIOS - HIPERMERCADOS E SUPERMERCADOS"] = 12
        self._dict[
            "- - - COMÉRCIO VAREJISTA DE MERCADORIAS EM GERAL, COM PREDOMINÂNCIA DE PRODUTOS ALIMENTÍCIOS - MINIMERCADOS, MERCEARIAS E ARMAZÉNS"] = 13
        self._dict["- - COMÉRCIO VAREJISTA DE PRODUTOS ALIMENTÍCIOS, BEBIDAS E FUMO"] = 14
        self._dict["- - COMÉRCIO VAREJISTA DE COMBUSTÍVEIS PARA VEÍCULOS AUTOMOTORES"] = 15
        self._dict["- - COMÉRCIO VAREJISTA DE MATERIAL DE CONSTRUÇÃO"] = 16
        self._dict["- - COMÉRCIO VAREJISTA DE EQUIPAMENTOS DE INFORMÁTICA E COMUNICAÇÃO; EQUIPAMENTOS E ARTIGOS DE USO DOMÉSTICO"] = 17
        self._dict["- - COMÉRCIO VAREJISTA DE ARTIGOS CULTURAIS, RECREATIVOS E ESPORTIVOS"] = 18
        self._dict["- - COMÉRCIO VAREJISTA DE PRODUTOS FARMACÊUTICOS, PERFUMARIA E COSMÉTICOS E ARTIGOS MÉDICOS, ÓPTICOS E ORTOPÉDICOS"] = 19
        self._dict["- - COMÉRCIO VAREJISTA DE PRODUTOS NOVOS NÃO ESPECIFICADOS ANTERIORMENTE E DE PRODUTOS USADOS"] = 20

        self._dict["DESOCUPADO"] = 21

        self._dict["- TRANSPORTE TERRESTRE"] = 22
        self._dict["- TRANSPORTE AQUAVIÁRIO"] = 23
        self._dict["- TRANSPORTE AÉREO"] = 24
        self._dict["- ARMAZENAMENTO E ATIVIDADES AUXILIARES DOS TRANSPORTES"] = 25
        self._dict["- CORREIO E OUTRAS ATIVIDADES DE ENTREGA"] = 26

        self._dict["NÃO DEFINIDO"] = 27

        self._dict["- ALOJAMENTO"] = 28
        self._dict["- ALIMENTAÇÃO"] = 29
        self._dict["INFORMAÇÃO E COMUNICAÇÃO"] = 30
        self._dict["ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS"] = 31
        self._dict["ATIVIDADES IMOBILIÁRIAS"] = 32
        self._dict["ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS"] = 33
        self._dict["ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES"] = 34
        self._dict["ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL"] = 35
        self._dict["EDUCAÇÃO"] = 36
        self._dict["SAÚDE HUMANA E SERVIÇOS SOCIAIS"] = 37
        self._dict["ARTES, CULTURA, ESPORTE E RECREAÇÃO"] = 38
        self._dict["ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS"] = 39
        self._dict["OUTRAS ATIVIDADES DE SERVIÇOS"] = 40

        self.name_to_label_2way = self._dict

    def get_label_with(self, key):
        return self._dict[key]


scheme = SchemeCNAE()



def description(landuse_description):
    return re.sub(r'[^a-zA-Z0-9\s]', '',
                  re.sub(r'[áãâà]', 'a',
                         re.sub(r'[éẽê3]', 'e',
                                re.sub(r'[íĩî1]', 'i',
                                       re.sub(r'[óõô0]', 'o',
                                              re.sub(r'[úũûü]', 'u',
                                                     re.sub(r'[ç]', 'c', str(landuse_description).lower())))))))


def label_to_int(manual_label):
    try_last = ["OBRAS", "CONSTRUÇÃO", "- COMÉRCIO VAREJISTA"]
    for key in scheme.name_to_label_2way:
        if type(key) is str and str(key) not in try_last:
            if str(key).lower() in str(manual_label).lower():
                return scheme.name_to_label_2way[key]
    for key in try_last:
        if key.lower() in str(manual_label).lower():
            return scheme.name_to_label_2way[key]
    return scheme.undefined


def label_str_to_int(df):
    classes = list(df['manual_label'].unique())
    for clss in classes:
        df.loc[df[df['manual_label'] == clss].index, 'label'] = label_to_int(clss)
    df['label'] = df['label'].astype(int)
    """
    # show unique labels
    for int_l in sorted(list(df['label'].unique())):
        print(f'{int_l}: {utils.scheme.name_to_label_2way[int_l]}')
    """


def get_label_name(num):
    return scheme.name_to_label_2way[num]
