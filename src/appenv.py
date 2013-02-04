#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'chenlong'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db'
app.debug = True

db = SQLAlchemy(app)
