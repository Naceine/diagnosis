"""Unit-Test for data processing pipelines.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: test_data.py
     Created on 02 June, 2019 @ 01:17 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""

# Built-in libraries.
import unittest

# custom libraries.
from config.consts import FS
from diagnosis.core import Data, File


class TestData(unittest.TestCase):
    def setUp(self):
        data_dir = File.join(FS.DATA_DIR,
                             ('HealthKnowledgeGraph/'
                              'DerivedKnowledgeGraph_final.csv'))
        self.data = Data(data_dir=data_dir)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
