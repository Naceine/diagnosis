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
from diagnosis.core.data import Data

if __name__ == '__main__':
    path = File.join(FS.DATA_DIR,
                     'HealthKnowledgeGraph/DerivedKnowledgeGraph_final.csv')
    data = Data(data_dir=path)
    Log.debug(data)
