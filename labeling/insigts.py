import pandas as pd
import cnae_scheme
from word_dists import dists


def main():
    dists.test_dists()
    print('\nPHONETIC:')
    print(dists.has_any_similar_phonetic_word(
        ['extracao', 'marmore', 'garimpo', 'mineracao', 'metais', 'metais',
         'manganes', 'titanio', 'niobio', 'aluminio', 'mineradora', 'carvao',
         'minerio', 'cobre', 'estanho', 'argila', 'areia', 'moedora', 'petrobras'], 'ABC COMERCIAL DE ALIMENTOS'))

    print('\nCHAR:')
    print(dists.has_any_similar_char_seq(['deus', 'fedex', 'sedex'], 'pao dos queijo'))

    cols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label', 'label', 'snorkel_category']
    dtype = {'order': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str,
             'label': str, 'manual_label': str, 'snorkel_category': int}

    with_dists = pd.read_csv('output/with-dists/labeled-sample-br-0.05-37625-semdup-manual-fix.csv', encoding='utf-8',
                             dtype=dtype, usecols=cols)
    no_dists = pd.read_csv('output/no-dists/labeled-no-dists-semdup-manual-fix.csv', encoding='utf-8', dtype=dtype,
                           usecols=cols)
    just_edit = pd.read_csv('output/just-edit/labeled-just-edit-semdup-manual-fix.csv', encoding='utf-8', dtype=dtype,
                            usecols=cols)
    just_sound = pd.read_csv('output/just-sound/labeled-just-sound-semdup-manual-fix.csv', encoding='utf-8',
                             dtype=dtype, usecols=cols)
    no_manual = pd.read_csv('output/no-manual/labeled-0.05-37625-no-manual.csv', encoding='utf-8', dtype=dtype,
                            usecols=cols)

    print(f'Labeled undefined => '
          f'no dists: {(no_dists["snorkel_category"] == -1).sum()} '
          f'| with dists:{(with_dists["snorkel_category"] == -1).sum()} '
          f'| just edit dist:{(just_edit["snorkel_category"] == -1).sum()} '
          f'| just sound dist:{(just_sound["snorkel_category"] == -1).sum()}'
          f'| no manual label rule:{(no_manual["snorkel_category"] == -1).sum()}.')


main()
