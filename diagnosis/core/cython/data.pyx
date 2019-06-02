"""Data processing pipeline.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: data.pyx
     Created on 02 June, 2019 @ 12:34 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""
# Built-in libraries.
import re

# Third-party libraries.
import pandas as pd

# Custom libraries.
from diagnosis.core.base import Base
from diagnosis.core.utils import Log


class Data(Base):
    def __init__(self, data_dir, **kwargs):
        super(Base, self).__init__(**kwargs)

        self.data_dir = data_dir


cpdef list process_features(str line):
    cdef list features = []
    cdef str symptoms_weights, symptom
    cdef float weight

    for symptoms_weights in line.split(', '):
        symptom = re.findall(r'^(\w+)', symptoms_weights)[0]
        weight = float(re.findall(r'\((.*?)\)',
                                  symptoms_weights)[0])
        features.append((symptom, weight))

    return features
