from flask import Flask
# from flask import flask_WTF
# from flask import flaskForm

import os

app = Flask(__name__)
app.static_folder = 'static'