"""`diagnosis.datasets` sub-package for loading datasets.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: __init__.py
     Package: diagnosis.datasets
     Created on 10 July, 2019 @ 02:22 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""


from . import dataset
from . import mqa_load_dataset
from . import tokenization


__all__ = [
    'dataset', 'mqa_load_dataset', 'tokenization',
]
