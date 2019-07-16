"""Code for running training experiments and selecting the best model.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: __init__.py
     Package: training
     Created on 10 July, 2019 @ 02:36 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""
from .train_data_to_embedding import train_data_to_embedding
from .train_embedding_to_gpt2_data import train_embedding_to_gpt2_data
from .train_ffn import train_ffn
from .train_bertffn import train_bertffn
from .train_gpt2 import train_gpt2
