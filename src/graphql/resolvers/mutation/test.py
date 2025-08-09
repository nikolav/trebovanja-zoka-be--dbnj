
from src.graphql.setup import mutation

from flask_app import db
# from src.models.docs   import Docs
# from src.models.tags   import Tags
# from src.models.orders import Orders
from src.models.assets import Assets

from src.schemas.serialization import SchemaSerializeAssets


@mutation.field('test')
def resolve_test(_o, _i):  
  _err, cli = db  
  
  a1 = cli.session.scalar(
    cli.select(
      Assets
    ).where(
      1 == Assets.id
    ))
  
  return SchemaSerializeAssets(many = True, exclude = ('assets_has',)).dump(
    Assets.assets_children(a1)) if a1 else []


