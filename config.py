import os
from app import app

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'rip rwap im taking a bath'

# database settings
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
                                username="simonja1",
                                password="Gazzapples612",
                                hostname="simonja1.mysql.pythonanywhere-services.com",
                                databasename="simonja1$tmc_db",
                                )
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_POOL_RECYCLE = 299

app.config['TESTING'] = False
app.config['LOGIN_DISABLED'] = False
