import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    db_user = os.environ.get('PGUSER')
    db_pass = os.environ.get('PGPASSWORD')
    db_local = os.environ.get('DATABASE_URL')
    WTF_CSRF_ENABLED = True

    # database settings
    SQLALCHEMY_DATABASE_URI = db_local
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
