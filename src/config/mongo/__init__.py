
from flask_pymongo import PyMongo

from src.config import Config


print('@mongodb:init')


initialized = False

client = None
error  = None

def mongodb_init(app):
  global client
  global error
  global initialized

  if not initialized:  
    try:
      client = PyMongo(app,
                       uri = Config.MONGODB_URI,
                      )

    except Exception as err:
      error = err
    
    initialized = True
  
  return error, client


