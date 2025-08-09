
from flask_sqlalchemy import SQLAlchemy

from src.utils.model_base import ModelBase


initialized = False
error       = None
cli         = None

def sqldb_init(app):
  global initialized
  global error
  global cli

  if not initialized:
    try:
      cli = SQLAlchemy(app, 
                      model_class = ModelBase,
                    )
    
    except Exception as e:
      error = e
    
    else:
      print('@debug --db:init')
  
  initialized = True
  
  return error, cli


