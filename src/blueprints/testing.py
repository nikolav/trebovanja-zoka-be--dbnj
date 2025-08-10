
from flask      import Blueprint
from flask_cors import CORS

from flask_app import db

from src.models.assets         import Assets
from src.schemas.serialization import SchemaSerializeAssets
# from src.config import Config


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  _err, dd = db
  a = dd.session.get(Assets, 1)
  return SchemaSerializeAssets(exclude = ('assets_has',)).dump(a) if a else []


