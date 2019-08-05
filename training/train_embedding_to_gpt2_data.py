"""Create the GPT-2 training data.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: train_embedding_to_gpt2_data.py
     Package: training
     Created on 5 August, 2019 @ 02:25 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""
import os

from glob import glob
from math import ceil
from collections import defaultdict

import faiss
import numpy as np
import pandas as pd

from tqdm import tqdm

from config.consts import FS

def train_embedding_to_gpt2_data(
        data_path=FS.EMBEDDINGS.BERT_FFN_ZIP,
        output_path=FS.EMBEDDINGS.BERT_FFN_GPT2,
        number_samples=10,
        batch_size=512,
        search_by='answer'):
    """Function to create gpt2 training data.

    For each question, we take number_samples similar question/answer pair as prefix of GPT2 model.
    For more details:
        https://github.com/Santosh-Gupta/DocProduct/blob/master/README.md

    Arguments:
        data_path {str} -- Embedding data path, usually the output file of train_data_to_embedding (default: {'qa_embeddings/bertffn_crossentropy.zip'})
        output_path {str} -- GPT2 training data output path (default: {'gpt2_train_data/bertffn_crossentropy_gpt2_train_data.zip'})
        number_samples {int} -- Number of sample per question (default: {10})
        batch_size {int} -- Retreive batch size of FAISS (default: {512})

    """
    _, ext = os.path.splitext(data_path)
    if ext == '.pkl':
        qa = pd.read_pickle(data_path)
    else:
        qa = pd.read_parquet(data_path)
    # qa = pd.read_parquet(data_path)

    question_bert = qa["Q_FFNN_embeds"].tolist()
    answer_bert = qa["A_FFNN_embeds"].tolist()
    question_bert = np.array(question_bert)
    answer_bert = np.array(answer_bert)

    question_bert = question_bert.astype('float32')
    answer_bert = answer_bert.astype('float32')

    answer_index = faiss.IndexFlatIP(answer_bert.shape[-1])
    question_index = faiss.IndexFlatIP(question_bert.shape[-1])

    faiss.normalize_L2(question_bert)
    faiss.normalize_L2(answer_bert)

    answer_index.add(answer_bert)
    question_index.add(question_bert)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df_dict = defaultdict(list)

    def topKforGPT2(start_ind, end_ind, topk, search_by):
        if search_by == 'answer':
            _, I1 = answer_index.search(
                question_bert[start_ind:end_ind].astype('float32'), topk)
            return I1
        else:
            _, I2 = question_index.search(
                question_bert[start_ind:end_ind].astype('float32'), topk)
            return I2

    steps = ceil(qa.shape[0] / batch_size)

    # for k in tqdm(range(1000), mininterval=30, maxinterval=60):
    for k in tqdm(range(0, qa.shape[0], batch_size), total=steps):
        start_ind = k
        end_ind = k + batch_size

        a_batch_index = topKforGPT2(start_ind, end_ind,
                                    int(number_samples),
                                    search_by=search_by)

        for i, a_index in enumerate(a_batch_index):
            df_dict['question'].append(qa["question"].iloc[k + i])
            df_dict['answer'].append(qa["answer"].iloc[k + i])

            for ii in range(number_samples):
                df_dict['question{0}'.format(ii)].append(
                    qa.question.iloc[a_index[ii]])
                df_dict['answer{0}'.format(ii)].append(
                    qa.answer.iloc[a_index[ii]])

    df = pd.DataFrame(df_dict)
    df.to_parquet(output_path, index=False)


if __name__ == "__main__":
    train_embedding_to_gpt2_data()
