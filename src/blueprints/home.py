
from flask      import Blueprint
from flask_cors import CORS
from sqlalchemy import text

from flask_app import redis_client
from flask_app import mongo
from flask_app import db

from src.config import Config


bp_home = Blueprint('home', __name__, url_prefix = '/')

# cors blueprints as wel for cross-domain requests
CORS(bp_home)

@bp_home.route('/', methods = ('GET',))
def status_ok():
  redis_version = None
  mongo_version = None
  db_version    = None

  try:
    if redis_client:
      _err_redis, client_redis = redis_client
      redis_version = client_redis.info().get('redis_version') if client_redis else ''
    
    if mongo:
      _err_mongo, client_mongo = mongo
      mongo_version = client_mongo.cx.server_info()['version'] if client_mongo else ''
    
    if db:
      _err_db, client_db = db
      db_version = client_db.session.execute(
            text("SELECT version();")
          ).scalar() if client_db else ''

  except:
    pass

  return {
    'status'   : 'ok',
    'app:name' : Config.APP_NAME,
    'db'       : db_version,
    'mongo'    : mongo_version,
    'redis'    : redis_version,
  }

