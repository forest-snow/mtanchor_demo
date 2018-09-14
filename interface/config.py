import os
basedir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = os.environ.get('SECRET_KEY') or '5e7f66fd2494e57869de'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False
