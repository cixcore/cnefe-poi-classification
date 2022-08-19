import pandas as pd
import cnae_scheme
import lf


def import_csv(filepath, dtype, usecols, finalcols):
    print(f'\nReading from file "{filepath}"...')
    df = pd.read_csv(f'{filepath}', encoding='utf-8', dtype=dtype, usecols=usecols)
    df.columns = finalcols
    return df


def get_label_name(int_key: int):
    if int_key in [cnae_scheme.scheme.undefined, cnae_scheme.scheme.undefined_labeled]:
        return "NÃO DEFINIDO"
    return cnae_scheme.scheme.get_label_with(int_key)


def main():
    finalcols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label']
    cols_original = ['ordem', 'urban_rural', 'landuse_id', 'landuse_description', 'categoria_cnae']
    dtype = {'order': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str, 'manual_label': str}
    dtype_original = {'ordem': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str, 'categoria_cnae': str}

    original = import_csv('input/sample-br-0.05-37625-semdup.csv', dtype_original, cols_original, finalcols)

    for filename in ['mismatched-1-auto-manual-diff', 'mismatched-2-undefined', 'mismatched-3-no-manual-label']:
        file = import_csv(f'fix/{filename}.csv', dtype, finalcols, finalcols)
        for index, row in file.iterrows():
            original_manual_label = original.loc[original['order'] == row.order]
            if str(original_manual_label.manual_label) != row.manual_label:
                print(f'Updating order {row.order}.')
                original.loc[original['order'] == row.order, 'manual_label'] = row.manual_label

    original.to_csv('fix/sample-br-0.05-37625-semdup-manual-fix.csv', index=False, encoding='utf-8')

    print('Done!')


main()
