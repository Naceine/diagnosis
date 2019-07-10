"""Distribution setup file to install & build libraries.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: setup.py
     Created on 2nd June, 2019 @ 12:45 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""

# Built-in libraries.
from distutils.core import setup


setup(
    name='diagnosis',
    version='1.0.0',
    url='https://github.com/victor-iyiola/diagnosis',
    license='BSD-3 Clause',
    author='Victor I. Afolabi',
    author_email='javafolabi@gmail.com',
    description="Medical Diagnosis System",
    long_description=open('README.md', mode='r', encoding='utf-8').read()
)
