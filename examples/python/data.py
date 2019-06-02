"""Example showcasing working with data.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: data.py
     Created on 02 June, 2019 @ 01:03 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""
from config.consts import FS
from diagnosis.core.utils import Log, File
import re


def process_features(line: str):
    features = []
    for symptoms_weights in line.split(', '):
        symptom = re.findall(r'^(\w+)', symptoms_weights)[0]
        weight = float(re.findall(r'\((.*?)\)',
                                  symptoms_weights)[0])
        features.append((symptom, weight))
    return features


if __name__ == '__main__':
    import pandas as pd

    path = File.join(FS.DATA_DIR,
                     'HealthKnowledgeGraph/DerivedKnowledgeGraph_final.csv')

    df = pd.read_csv(path)
    features = df['Symptoms'].map(process_features)
    labels = df['Diseases'].values
    Log.debug(features.head())
