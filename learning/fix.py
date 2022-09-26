import utils
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    """
    manual_df = pd.read_csv('./sample-br-0.05-37625-manual-labeled.csv', encoding='utf-8',
                            dtype={'order': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str,
                                   'manual_label': str},
                            usecols=['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label'])
    manual_df = manual_df[manual_df['manual_label'].notna()]

    manual_df.to_csv(f'./manual-annotation-0.05-37625.csv', encoding='utf-8', index=False)
    
    #######
    df = pd.read_csv('./manual-annotation-0.05-37625.csv', encoding='utf-8',
                     dtype={'order': int, 'urban_rural': int, 'landuse_id': int, 'landuse_description': str,
                            'manual_label': str},
                     usecols=['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label'])
    # string classes to int
    utils.label_str_to_int(df)
    df.reset_index(drop=True, inplace=True)
    df = df.drop_duplicates(['landuse_id', 'landuse_description', 'manual_label'])
    print(len(df))

    df['label'] = df['manual_label'].apply(lambda x: utils.label_to_int(x))

    df2 = df.groupby('label').count()
    df2 = df2.rename(columns={'landuse_description': 'Count'})
    df2.index.name = 'Label'
    print(df2)
    df2.to_csv(f'./manual_label_dist_br.csv', encoding='utf-8')
    sns.barplot(x=df2.index, y=df2['Count'], data=df2).tick_params(labelsize=5)
    plt.savefig('manual_label_dist.pdf')
    #######

    """
    df = pd.read_csv('./bert-training/labeled-br.csv', encoding='utf-8',
                     dtype={'landuse_description': str, 'label': str, 'pred_label': int},
                     usecols=['landuse_description', 'label', 'pred_label'])

    # string classes to int
    print(len(df))

    df2 = df.groupby('pred_label').count()
    df2 = df2.rename(columns={'label': 'Count (by million)'})
    df2.index.name = 'Label'
    print(df2)
    df2.to_csv(f'./bert-training/label_dist_bert_br.csv', encoding='utf-8')
    sns.barplot(x=df2.index, y=df2['Count (by million)'], data=df2).tick_params(labelsize=5)
    plt.savefig('./bert-training/label_dist_bert_br.pdf')
    #######

    """
    df = pd.read_csv('../labeling/output/br/snorkel-just-phonetic/labeled.csv', encoding='utf-8',
                     dtype={'landuse_description': str, 'label': str},
                     usecols=['landuse_description', 'label'])

    # string classes to int
    print(len(df))
    df['pred_label'] = df['label'].apply(lambda x: utils.label_to_int(x))

    df2 = df.groupby('pred_label').count()
    df2 = df2.rename(columns={'label': 'Count (by million)'})
    df2.index.name = 'Label'
    print(df2)
    df2.to_csv(f'./label_dist_snorkel_br.csv', encoding='utf-8')
    sns.barplot(x=df2.index, y=df2['Count (by million)'], data=df2).tick_params(labelsize=5)
    plt.savefig('./label_dist_snorkel_br.pdf')
    """
