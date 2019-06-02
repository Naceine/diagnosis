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
from config.config import Config

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

    # Resources & data directories.
    RESOURCE_DIR = os.path.join(PROJECT_DIR, 'resources')
    CACHE_DIR = os.path.join(RESOURCE_DIR, 'cache')
    DATA_DIR = os.path.join(RESOURCE_DIR, 'data')


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
