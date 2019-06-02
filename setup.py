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
import platform
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

# Custom libraries.
from config import FS

# Compiler & Linker flags.
compile_extra_args = []
link_extra_args = []

# Platform specific flags.
if platform.system() == "Windows":
    compile_extra_args = ["/std:c++latest", "/EHsc"]
elif platform.system() == "Darwin":
    compile_extra_args = ['-std=c++17', "-mmacosx-version-min=10.9"]
    link_extra_args = ["-stdlib=libc++", "-mmacosx-version-min=10.9"]

# Cython extension modules.
ext_modules = [
    # Cython.
    Extension(name="*",
              language="c++",
              sources=[
                  'diagnosis/core/cython/**/*.pyx',
              ],
              include_dirs=[FS.INCLUDE_DIR, ],
              extra_compile_args=compile_extra_args,
              extra_link_args=link_extra_args),
]

# Compiler directives
compiler_directives = {
    'language_level': 3,
    'always_allow_keywords': True,
}

setup(
    name='diagnosis',
    version='1.0.0',
    # packages=[],
    requires=['Cython'],
    package_data={
        'diagnosis/core': ['diagnosis/core/cython/**/*.pxd',
                           'diagnosis/core/cython/**/*.pyx'],
    },
    ext_modules=cythonize(ext_modules,
                          compiler_directives=compiler_directives),
    url='https://github.com/victor-iyiola/diagnosis',
    license='BSD-3 Clause',
    author='Victor I. Afolabi',
    author_email='javafolabi@gmail.com',
    description="Medical Diagnosis System",
    long_description=open('README.md', mode='r', encoding='utf-8').read()
)
