import pandas as pd
import cnae_scheme
from word_dists import dists


def main():
    dists.test_dists()
    print('\nPHONETIC:')
    print(dists.has_any_similar_phonetic_word(['baldio', 'abandonado', 'inoperante', 'fechado',
                                               'fechada', 'falido', 'desocupada', 'abandonada',
                                               'antiga'], 'WISE UP E ANNA K BEAUTY CARE'))
    print(dists.has_any_similar_phonetic_word(['jesus', 'cristo', 'ogum', 'iemanja', 'exu', 'oxala', 'omulu',
                                               'oxum', 'batista', 'catedral', 'xango', 'orixa', 'igreja', 'templo',
                                               'espirita', 'espirito', 'espiritual', 'espiritualidade', 'wesleyana',
                                               'catolica', 'evangelica', 'umbanda', 'candomble', 'judaica', 'sinagoga',
                                               'capela', 'catequetico'], 'AFRESP ASSOCIACAO DOS AGENTES FISCAIS RE'))
    print('\nCHAR:')
    print(dists.has_any_similar_char_seq(['deus', 'fedex', 'sedex'], 'pao dos queijo'))

    cols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label', 'label', 'snorkel_category']
    dtype = {'order': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str,
             'label': str, 'manual_label': str, 'snorkel_category': int}

    with_dists = pd.read_csv('output/with-dists/labeled-sample-br-0.05-37625-semdup-manual-fix.csv', encoding='utf-8', dtype=dtype, usecols=cols)
    no_dists = pd.read_csv('output/no-dists/labeled-no-dists-semdup-manual-fix.csv', encoding='utf-8', dtype=dtype, usecols=cols)

    print(f'Labeled undefined => '
          f'no dists: {(no_dists["snorkel_category"] == -1).sum()} '
          f'| with dists:{(with_dists["snorkel_category"] == -1).sum()}.')


main()
