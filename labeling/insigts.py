import pandas as pd
import cnae_scheme


def main():
    cols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label', 'label', 'snorkel_category']
    dtype = {'order': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str,
             'label': str, 'manual_label': str, 'snorkel_category': int}

    with_dists = pd.read_csv('output/with-dists/labeled-sample-br-0.05-37625-semdup-manual-fix.csv', encoding='utf-8', dtype=dtype, usecols=cols)
    no_dists = pd.read_csv('output/no-dists/labeled-no-dists-semdup-manual-fix.csv', encoding='utf-8', dtype=dtype, usecols=cols)

    print(f'Labeled undefined => '
          f'no dists: {(no_dists["snorkel_category"] == -1).sum()} '
          f'| with dists:{(with_dists["snorkel_category"] == -1).sum()}.')


main()
