"""`diagnosis.networks` - for building neural networks (i.e., 'dumb' input -> output mappings) used by models.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: __init__.py
     Package: diagnosis.networks
     Created on 10 July, 2019 @ 02:29 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""

from .keras_bert.tokenizer import Tokenizer
from .keras_bert.loader import (build_model_from_config,
                                load_model_weights_from_checkpoint,
                                load_trained_model_from_checkpoint)
from .keras_bert.bert import (TOKEN_PAD, TOKEN_UNK, TOKEN_CLS, TOKEN_SEP, TOKEN_MASK,
                              gelu, get_model, get_custom_objects, get_base_dict, gen_batch_inputs)


__all__ = [
    # Keras BERT Model.
    'TOKEN_PAD', 'TOKEN_UNK', 'TOKEN_CLS', 'TOKEN_SEP', 'TOKEN_MASK',
    'gelu', 'get_model', 'get_custom_objects', 'get_base_dict', 'gen_batch_inputs',
    'build_model_from_config', 'load_model_weights_from_checkpoint', 'load_trained_model_from_checkpoint',
    'Tokenizer',
]
