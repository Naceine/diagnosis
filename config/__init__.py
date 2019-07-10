"""Configuration package.

   @author
     Victor I. Afolabi
     Artificial Intelligence & Software Engineer.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: __init__.py
     Package: config
     Created on 2nd June, 2019 @ 12:16 PM.

   @license
     BSD-3 Clause License
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""

# File system.
from config.consts import FS, LOGGER, SETUP

# Configuration utils.
from config.config import Config

# Utilities.
from config.util import Downloader, File, Log, Cache

__all__ = [
    # Configuration utils.
    'Config',

    # Utilities.
    'Downloader', 'File', 'Log', 'Cache',

    # File system configurations.
    'FS', 'SETUP', 'LOGGER',
]
