
from src.graphql.setup import mutation

from flask_app import db
from src.models.docs   import Docs
from src.models.tags   import Tags
from src.models.assets import Assets
from src.models.orders import Orders

from src.schemas.serialization import SchemaSerializeAssets


@mutation.field('test')
def resolve_test(_o, _i):  
  _err, cli = db  
  
  o1 = Orders()
  o1.tags_add('lorem:2')
  cli.session.add(o1)
  cli.session.commit()
  
  return []

