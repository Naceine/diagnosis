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
from diagnosis.core.base import Base


class Data(Base):
    def __init__(self, data_dir, **kwargs):
        super(Base, self).__init__(**kwargs)

        self.data_dir = data_dir
