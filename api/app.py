"""Flask Web server that serves predictions.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: app.py
     Package: api
     Created on 10 July, 2019 @ 02:19 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""
from flask import Flask

# Create flask app.
app = Flask(__name__)

# App confnigurations.
app.config.from_pyfile('config.cfg', silent=True)
app.config.from_object('config.Development')
