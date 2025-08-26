
import os

from flask          import Flask
from flask_cors     import CORS
from flask_talisman import Talisman

from src.config import Config


FLASKAPP_PATH = os.path.dirname(__file__)

app = Flask(__name__,
            template_folder = Config.FLASK_TEMPLATES_FOLDER,
            )

app.config['SECRET_KEY'] = Config.SECRET_KEY

app.config['REDIS_URL'] = Config.REDIS_URL

app.config['SQLALCHEMY_DATABASE_URI']        = Config.DATABASE_URI_production if Config.PRODUCTION else Config.DATABASE_URI_development
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']                = not Config.PRODUCTION or Config.SQLALCHEMY_ECHO


# services:redis
redis_client = None
if Config.REDIS_INIT:
  from src.config.redis import redis_init
  redis_client = redis_init(app)

# db:mongo
mongo = None
if Config.MONGODB_INIT:
  from src.config.mongo import mongodb_init
  mongo = mongodb_init(app)

# db:sql
db = None
if Config.DB_INIT:
  from src.config.db import sqldb_init
  db = sqldb_init(app)

  with app.app_context():
    from src.config.db.models_init import models_init
    models_init(db)

    # setup tables
    import src.config.db.tables_init

# services:io
#  realtime support
from src.config.io import socketio_setup
io = socketio_setup(app)

# services:cors
from src.config.cors import cors_resources
CORS(app, 
    resources = cors_resources if Config.PRODUCTION else { r'.*': { 'origins': '*' } },
    supports_credentials = True, 
  )

# services:talisman
#  content security headers
Talisman(app, 
         force_https=False,
        )

# services:firebase
if Config.FIREBASEADMIN_INIT:
  import src.config.firebase_admin


# route:graphql, @[`POST /graphql`]
from src.graphql.setup import graphql_mount_endpoint
graphql_mount_endpoint(app)

# mount route:home [@/]
from src.blueprints.home import bp_home
app.register_blueprint(bp_home)

# mount route:auth [@/auth]
from src.blueprints.auth import bp_auth
app.register_blueprint(bp_auth)

# mount route:home [@/]
if not Config.PRODUCTION:
  from src.blueprints.testing import bp_testing
  app.register_blueprint(bp_testing)


# middleware:before
from src.middleware.auth import authenticate
@app.before_request
def handle_before_request():
  return authenticate()


