import pandas as pd

# 'mismatched-1-auto-manual-diff', 'mismatched-2-undefined', 'mismatched-3-no-manual-label', 'mismatched-4-updated'

def import_csv(filepath, dtype, usecols, final_cols):
    print(f'\nReading from file "{filepath}"...')
    df = pd.read_csv(f'{filepath}', encoding='utf-8', dtype=dtype, usecols=usecols)
    df.columns = final_cols
    return df


final_cols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label']
labeled_cols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label', 'pred_label', 'snorkel_category']
original_cols = ['ordem', 'urban_rural', 'landuse_id', 'landuse_description', 'categoria_cnae']
dtype = {'order': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str, 'manual_label': str}
dtype_labeled = {'order': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str, 'manual_label': str, 'pred_label': str, 'snorkel_category': int}
dtype_original = {'ordem': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str, 'categoria_cnae': str}


def main():
    # original = import_csv('../input/sample-br-0.05-37625-fix.csv', dtype, final_cols, final_cols)
    original = import_csv('../output/no-manual/labeled-br-0.05-37625.csv', dtype_labeled, labeled_cols, labeled_cols)
    # original = import_csv('../input/sample-br-0.05-37625-semdup-manual-fix.csv', dtype_original, original_cols, final_cols)

    for filename in ['mismatched-7-updated']:
        file = import_csv(f'./{filename}.csv', dtype, final_cols, final_cols)
        for index, row in file.iterrows():
            original_manual_label = original.loc[original['order'] == row.order].iloc[0]
            if str(original_manual_label.manual_label) != str(row.manual_label):
                print(f'Updating order {row.order}')
                # print(f'str(original_manual_label.manual_label): {str(original_manual_label.manual_label)}.')
                # print(f'row.manual_label: {row.manual_label}.')
                # print(f'Equals: {str(original_manual_label.manual_label) != row.manual_label} | {str(original_manual_label.manual_label) != str(row.manual_label)}.')
                original.loc[original['order'] == row.order, 'manual_label'] = row.manual_label

    original.to_csv('./labeled-br-0.05-37625.csv', index=False, encoding='utf-8')

    print('Done!')


main()
