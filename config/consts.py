"""Configuration - constants.

   @author
     Victor I. Afolabi
     Artificial Intelligence & Software Engineer.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: consts.py
     Created on 26 January, 2018 @ 01:11 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""
# Built-in libraries.
import os.path
from abc import ABCMeta
from collections import namedtuple

# Custom libraries.
from .config import Config

# Exported configurations.
__all__ = [
    'FS', 'LOGGER', 'SETUP',
]


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | FS: File System.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class FS(metaclass=ABCMeta):
    # Project name & absolute directory.
    PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
    APP_NAME = os.path.basename(PROJECT_DIR)

    # Directory to save stuffs.
    CONFIG_DIR = os.path.join(PROJECT_DIR, 'config')

    # Libraries & Include folders.
    LIB_DIR = os.path.join(PROJECT_DIR, 'diagnosis')
    ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')
    DATA_DIR = os.path.join(ASSETS_DIR, 'data')
    MODEL_DIR = os.path.join(ASSETS_DIR, 'models')

    # Data folder.
    __DataDir = namedtuple('__DataDir', ['MQA'])
    DATA = __DataDir(MQA=os.path.join(DATA_DIR, 'mqa_csv'))

    # Model folders.
    __ModelDir = namedtuple(
        '__ModelDir', ['GPT2', 'BIO_BERT', 'FFN', 'BERT_FFN'])
    MODELS = __ModelDir(GPT2=os.path.join(MODEL_DIR, 'gpt2'),
                        BIO_BERT=os.path.join(MODEL_DIR, 'bio_bert'),
                        FFN=os.path.join(MODEL_DIR, 'ffn_crossentropy/ffn'),
                        BERT_FFN=os.path.join(MODEL_DIR,
                                              'bertffn_crossentropy/bertffn'))

    # Pre-trained folders.
    __PreTrainedDir = namedtuple('__PreTrainedDir', ['GPT2', 'PUB_MED'])
    PRE_TRAINED = __PreTrainedDir(GPT2=os.path.join(MODEL_DIR, '117M'),
                                  PUB_MED=os.path.join(MODEL_DIR, 'pubmed_pmc_470k'))


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | DOWNLOADS: Data URL, Resource URLs & File IDs.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class DOWNLOADS(metaclass=ABCMeta):
    G_DRIVE_BASE = 'https://docs.google.com/uc?export=download'

    __Web = namedtuple('__Web', ['PUB_MED'])
    WEB = __Web(PUB_MED=('https://github.com/naver/biobert-pretrained/''releases'
                         '/download/v1.0-pubmed-pmc/biobert_pubmed_pmc.tar.gz'))

    # Google Drive File Ids.
    __FileId = namedtuple('__FileId', ['FFN_DATA', 'FFN_INDEX', 'FFN_CKPT',
                                       'BERT_FFN_DATA', 'BERT_FFN_INDEX', 'BERT_FNN_CKPT',
                                       'FLOAT16_EMBED', 'FLOAT16_EMBED_EXPAND'])
    FILE_ID = __FileId(
        # FFN checkpoint files.
        FFN_DATA='1-258Wlpp5UwwqCPezy6DRYBozO4wBUBw',
        FFN_INDEX='1-9JmtJJ_XGV0wClZxs2Px4hDL-Pi9YA_',
        FFN_CKPT='1-5hczUjQfCTpBg1HhpLrgXFTkve1xuRM',
        # Bert-FFN checkpoint files.
        BERT_FFN_DATA='1thX75_cMkly5btgxTydgV6YDKnrUczZs',
        BERT_FFN_INDEX='11q29T38EysVPueD1PMQzZoKs5QFr3jRT',
        BERT_FFN_CKPT='1iI5Aow_7pQSmvpxGnMVKw9OJV-nckkxz',
        # Embedding files.
        FLOAT16_EMBED='1blkZdV1BNWesD0mJ6Pm1H1IhCMYThkWJ',
        FLOAT16_EMBED_EXPAND='1jnRRljMv752su76j6aLWIyHD5oo6itMN',
    )

################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Setup configuration constants.
# +--------------------------------------------------------------------------------------------+
################################################################################################


class SETUP(metaclass=ABCMeta):
    # Global setup configuration.
    __global = Config.from_cfg(os.path.join(FS.CONFIG_DIR,
                                            "setup/global.cfg"))
    # Build mode/type.
    MODE = __global['config']['MODE']


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Logger: Logging configuration paths.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class LOGGER(metaclass=ABCMeta):
    # Root Logger:
    ROOT = os.path.join(FS.CONFIG_DIR, f'logger/{SETUP.MODE}.cfg')

    # Another logger goes here: (and updated in diagnosis/core/utils.pyi)
