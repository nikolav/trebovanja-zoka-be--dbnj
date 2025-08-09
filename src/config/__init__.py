import os
import re

from dotenv import load_dotenv


load_dotenv()


ENV_ = os.getenv('ENV')
DEVELOPMENT_ = 'development' == ENV_
PRODUCTION_  = 'production'  == ENV_

class Config:

  ENV         = ENV_
  DEVELOPMENT = DEVELOPMENT_
  PRODUCTION  = PRODUCTION_
  PORT        = os.getenv('PORT')
  
  SECRET_KEY = os.getenv('SECRET_KEY')
  
  MESSAGE = os.getenv('MESSAGE')
  
  # keys
  KEY_TOKEN_CREATED_AT = '@'
  
  # paths
  FLASK_TEMPLATES_FOLDER     = os.getenv('FLASK_TEMPLATES_FOLDER')
  CATEGORY_KEY_ASSETS_prefix = os.getenv('CATEGORY_KEY_ASSETS_prefix')

  # cache:redis
  REDIS_INIT = bool(os.getenv('REDIS_INIT'))
  REDIS_URL  = os.getenv('REDIS_URL')

  # io:cors
  IO_CORS_ALLOW_ORIGINS = re.split(r'\s+', os.getenv('IO_CORS_ALLOW_ORIGINS').strip())

  # io
  IOEVENT_REDIS_CACHE_KEY_UPDATED_prefix = os.getenv('IOEVENT_REDIS_CACHE_KEY_UPDATED_prefix')
  
  # jwt
  JWT_EXPIRE_SECONDS      = int(os.getenv('JWT_EXPIRE_SECONDS'))
  JWT_SECRET_ACCESS_TOKEN = os.getenv('JWT_SECRET_ACCESS_TOKEN')

  # db:mongo
  MONGODB_INIT = bool(os.getenv('MONGODB_INIT'))
  MONGODB_URI = os.getenv('MONGODB_URI_production') if PRODUCTION_ else os.getenv('MONGODB_URI_development')

  # cloud messaging
  CLOUD_MESSAGING_INIT        = bool(os.getenv('CLOUD_MESSAGING_INIT'))
  CLOUD_MESSAGING_CERTIFICATE = os.getenv('CLOUD_MESSAGING_CERTIFICATE')

  # db
  DB_INIT                       = bool(os.getenv('DB_INIT'))
  DATABASE_URI_development      = os.getenv('DATABASE_URI_development')
  DATABASE_URI_production       = os.getenv('DATABASE_URI_production')
  TABLE_NAME_SUFFIX_dev         = os.getenv('TABLE_NAME_SUFFIX_dev')
  TABLE_NAME_SUFFIX_production  = os.getenv('TABLE_NAME_SUFFIX_production')
  SQLALCHEMY_ECHO               = bool(os.getenv('SQLALCHEMY_ECHO'))
  REBUILD_SCHEMA                = bool(os.getenv('REBUILD_SCHEMA'))


