import pandas as pd
from geobr import read_state
import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--data_path', type=str, default='./data', help='path to states csv')
    parser.add_argument('-g', '--rerun_geobr', action='store_const', const=True,
                        help='reruns geobr.read_state instead of using hardcoded abbreviations')
    parser.add_argument('-o', '--output_file', type=str, default='sample-BR-0.05.csv',
                        help='csv filename with the samples from all states')
    parser.add_argument('-a', '--do_states_append', action='store_const', const=True,
                        help='append all states in a single .csv')
    parser.add_argument('-p', '--percentage', type=float, default=0.05,
                        help='percentage of each data file to form the complete sample')
    parser.add_argument('-s', '--seed', type=int, default=0,
                        help='defines seed to be used in sample.random_state to reproduce results')
    return parser.parse_args()


def import_csv(path, state):
    print(f'\nReading from file "{path}/{state}.csv"...')
    dtype = {'uf': int, 'municipality': int, 'district': int, 'sub_district': int, 'tract': int,
             'urban_rural': int, 'place': str, 'address_1': str, 'address_2': str, 'house_number': int,
             'modifier': str, 'complement1': str, 'value_1': str, 'complement_2': str, 'value_2': str,
             'complement_3': str, 'value_3': str, 'complement4': str, 'value_4': str, 'complement_5': str,
             'value_5': str, 'complement_6': str, 'value_6': str, 'latitude': str, 'longitude': str,
             'borough': str, 'nil': str, 'landuse_id': int, 'landuse_description': str, 'multiple': str,
             'collective_name': str, 'block_number': int, 'face_number': int, 'post_code': int,
             'code_tract': float}
    return pd.read_csv(f'{path}/{state}.csv', encoding='latin-1', dtype=dtype)


def get_sample(percentage, seed, data_frame):
    if seed != 0:
        print(f'Sampling {percentage * 100}% of filtered rows (seed={seed}).')
        return data_frame.sample(frac=percentage, random_state=seed)
    else:
        print(f'Sampling {percentage * 100}% of filtered rows.')
        return data_frame.sample(frac=percentage)


def filter_by_landuse_id(data_frame):
    residencies = 1
    ongoing_construction = 7
    filtered = data_frame[~data_frame.landuse_id.isin([residencies, ongoing_construction])]
    print(f'Filtered rows that are not residencies or ongoing constructions.')
    return filtered


def add_to_csv(sample, filepath, used_columns):
    print(f'Appending to {filepath}.')
    with open(filepath, 'a') as f:
        sample.to_csv(f, mode='a', header=f.tell() == 0, columns=used_columns, index=False)


def states(rerun_geobr):
    if rerun_geobr:
        return read_state().abbrev_state.values
    else:
        return ['RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO', 'MA', 'PI',
                'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA', 'MG', 'ES',
                'RJ', 'SP', 'PR', 'SC', 'RS', 'MS', 'MT', 'GO', 'DF']


def main():
    args = parse_args()

    for state in states(args.rerun_geobr):
        state_data = import_csv(args.data_path, state)
        if args.do_states_append:
            add_to_csv(state_data, 'BR.csv', state_data.columns.tolist())
        else:
            filtered = filter_by_landuse_id(state_data)
            state_sample = get_sample(args.percentage, args.seed, filtered)
            h = ['uf', 'municipality', 'district', 'sub_district', 'urban_rural', 'landuse_id', 'landuse_description']
            add_to_csv(state_sample, args.output_file, h)


# python3 sample.py -s 37625 -o sample-BR-0.05-37625.csv
main()
