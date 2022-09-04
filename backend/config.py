import os
SECRET_KEY = os.urandom(32)
WTF_CSRF_SECRET_KEY = os.urandom(64)
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:lol@localhost:5432/trivia'
SQLALCHEMY_TRACK_MODIFICATIONS = True
