import os
import connexion
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# init connexion app
connex_app = connexion.App(__name__, specification_dir=BASE_DIR)

app = connex_app.app

pg_uri = 'postgresql+psycopg2://noyoapi:noyo@db:5432/noyo'

# SQLAlchemy conf
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = pg_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init SQLAlchemy db
db = SQLAlchemy(app)
