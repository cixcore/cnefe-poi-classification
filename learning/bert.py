import os
import math
import nltk
import utils
import torch
import random
import shutil
import pathlib
import logging
import numpy as np
import pandas as pd
from tqdm import tqdm
from tqdm import trange
from joblib import dump, load
from nltk import word_tokenize
from collections import Counter
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, f1_score, classification_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


class ClassificationDataset(Dataset):
    def __init__(self, docs):
        self.items = docs

    def __getitem__(self, idx):
        item = self.items.iloc[idx]
        text = item['text_enc']
        return {
            'input_ids': text['input_ids'],
            'token_type_ids': text['token_type_ids'],
            'attention_mask': text['attention_mask'],
            'labels': item['label']
        }

    def __len__(self):
        return len(self.items)


def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)

    f1_micro = f1_score(labels, preds, average='micro')
    # f1_w = f1_score(labels, preds, average='weighted')
    f1_macro = f1_score(labels, preds, average='macro')

    # precision, recall, f1_ma, _ = precision_recall_fscore_support(labels, preds, average='macro')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1-macro': f1_macro,
        'f1-micro': f1_micro
        # 'f1-weighted': f1_w,
        # 'precision': precision,
        # 'recall': recall
    }


def get_last_checkpoint(ckpt_path, logger):
    max_ckpt_step = 0
    if os.path.isdir(ckpt_path):
        dirs = []
        for model_path in os.listdir(ckpt_path):
            if model_path[:10] != 'checkpoint':
                continue
            ckpt_step = int(model_path.split("-")[-1].split("/")[0])
            if ckpt_step > max_ckpt_step:
                max_ckpt_step = ckpt_step
    if max_ckpt_step > 0:
        logger.info(f'Found checkpoint: {max_ckpt_step}')
        return os.path.join(ckpt_path, f'checkpoint-{max_ckpt_step}')
    else:
        logger.warning(f'No previous checkpoints was found in {ckpt_path}')
        return None


def test_report(trainer, test_dataset, train, val, training_args):
    p = trainer.predict(test_dataset)
    preds = p[0].argmax(-1)
    true_values = list(test_dataset.items['label'])
    df_train = train.copy()
    df_train = df_train.append(val)
    dic = classification_report(true_values, preds, output_dict=True)
    print('*****************  dados ***************************')
    print(f'LEN TRAIN: {len(train)} \t Classes: {Counter(train.label)}')
    print(f'LEN VAL  : {len(val)} \t Classes: {Counter(val.label)}')
    print(f'LEN TEST : {len(test)} \t Classes: {Counter(test.label)}')
    print('\n*****************  parametros ***************************')
    print('Learning rate: ', training_args.learning_rate)
    print('batch_size: ', training_args.train_batch_size)
    print('nr de steps em uma época: ', len(train) / training_args.train_batch_size)
    print('max_steps: ', training_args.max_steps)
    print('MODELO: ', MODEL)
    print('\n*****************  resultados por classe ***************************')
    print(classification_report(true_values, preds))
    f1_mi = f1_score(true_values, preds, average='micro')
    f1_ma = f1_score(true_values, preds, average='macro')
    acc = accuracy_score(true_values, preds)
    precision, recall, f1_ma2, _ = precision_recall_fscore_support(true_values, preds, average='macro')
    print('\n*****************  resultados gerais ***************************')
    print('Precision: ', precision)
    print('Recall: ', recall)
    print('F1-macro: ', f1_ma)
    print('F1-micro: ', f1_mi)
    print('Accuracy: ', acc)
    return dic, f1_ma, f1_mi, preds, true_values


directory = '.'
filename = 'sample-br-0.05-37625-manual-labeled.csv'

# le dados
cols = ['order', 'urban_rural', 'landuse_id', 'landuse_description', 'manual_label']
df = pd.read_csv(f"{directory}/{filename}", encoding='utf-8', sep=',', usecols=cols)
print(len(df))

df = df[df['landuse_description'].notna()]
df = df[df['manual_label'].notna()]
df['landuse_description'] = df['landuse_description'].map(utils.description)
df = df.rename(columns={'landuse_description': 'text'})
df = df.reset_index(drop=True)

df['count_tokens'] = df['text'].apply(lambda x: len(word_tokenize(x)))
print(df['count_tokens'].max())
MAX_TOKEN = 64

utils.label_str_to_int(df)
df.reset_index(drop=True, inplace=True)

X = df.index
y = list(df['label'])
X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.30, random_state=1, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.20, random_state=1,
                                                  stratify=y_train_full)

train = df.loc[X_train]
val = df.loc[X_val]
test = df.loc[X_test]

train = train.reset_index(drop=True)
val = val.reset_index(drop=True)
test = test.reset_index(drop=True)

MODEL = 'bert-base-multilingual-uncased'
tokenizer = BertTokenizer.from_pretrained(MODEL, do_lower_case=True)
MAX_TOKENS = 64

train['text_enc'] = train['text'].apply(
    lambda x: tokenizer(x, max_length=MAX_TOKENS, truncation=True, padding='max_length'))
val['text_enc'] = val['text'].apply(
    lambda x: tokenizer(x, max_length=MAX_TOKENS, truncation=True, padding='max_length'))
test['text_enc'] = test['text'].apply(
    lambda x: tokenizer(x, max_length=MAX_TOKENS, truncation=True, padding='max_length'))

# checando que gerou a codificação
print(train.loc[0, 'text_enc'])

train_dataset = ClassificationDataset(train)
val_dataset = ClassificationDataset(val)
test_dataset = ClassificationDataset(test)

output_dir = f"./bert-training"

batch_size = 32
epochs = 3
MAX_STEPS = math.ceil(len(train) / batch_size) * epochs
eval_steps = math.ceil(MAX_STEPS / min(25, len(train)))
hidden_dropout_prob = 0.1
learning_rate = 4e-05
attention_probs_dropout_prob = hidden_dropout_prob
num_labels = len(list(df['manual_label'].unique()))

training_args = TrainingArguments(
    output_dir=f'{output_dir}/ckpts',
    save_total_limit=1,
    max_steps=MAX_STEPS,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    learning_rate=learning_rate,
    do_eval=True,
    warmup_steps=100,
    save_steps=eval_steps,
    eval_steps=eval_steps,
    evaluation_strategy='steps',
    logging_steps=eval_steps,
    load_best_model_at_end=True,
    metric_for_best_model='eval_loss',  # 'f1-macro',
    greater_is_better=False  # True
)

model = BertForSequenceClassification.from_pretrained(
    MODEL,
    hidden_dropout_prob=hidden_dropout_prob,
    attention_probs_dropout_prob=attention_probs_dropout_prob,
    num_labels=num_labels
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
    # callbacks = [EarlyStoppingCallback(early_stopping_patience=3)] #early_stopping_threshold=0.00001
)
last_ckpt = get_last_checkpoint(f'{output_dir}/ckpts', logger)  # usa se tiver caido no meio
trainer.train(resume_from_checkpoint=last_ckpt)

dump(trainer, f'{output_dir}')

dic, f1_ma, f1_mi, preds, true_values = test_report(trainer, test_dataset, train, val, training_args)
print((dic, f1_ma, f1_mi, preds, true_values))
