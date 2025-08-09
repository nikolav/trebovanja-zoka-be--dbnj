
from src.config import Config

def models_init(db):
    _err, cli = db

    from src.models.docs   import Docs
    from src.models.tags   import Tags
    from src.models.assets import Assets
    from src.models.orders import Orders

    # drop/create schema
    if Config.REBUILD_SCHEMA:
      cli.drop_all()
    
    # create schema
    cli.create_all()


