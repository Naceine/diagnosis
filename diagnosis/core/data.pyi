"""Data processing pipeline.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: data.pyi
     Created on 02 June, 2019 @ 12:38 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""
# Built-in libraries.
from typing import Any

# Custom libraries.
from diagnosis.core.base import Base


class Data(Base):
    def __init__(self, data_dir: str, **kwargs: Any): ...
