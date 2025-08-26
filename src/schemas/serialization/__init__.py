
import json
from bson import ObjectId

# https://marshmallow.readthedocs.io/en/stable/quickstart.html#field-validators-as-methods
from marshmallow import Schema
from marshmallow import fields
from marshmallow import ValidationError
from marshmallow import INCLUDE


class SchemaSerializeTimes(Schema):
  created_at = fields.DateTime()
  updated_at = fields.DateTime()


class SchemaSerializeDocs(SchemaSerializeTimes):
  id   = fields.Integer()
  data = fields.Dict()
  key  = fields.String()


class SchemaSerializeAssetsTextSearch(Schema):
  name       = fields.String()
  code       = fields.String()
  location   = fields.String()
  notes      = fields.String()
  key        = fields.String()
  tags       = fields.Method('tags_joined')
  data_dumps = fields.Method('resolve_data_dumps')
  
  def tags_joined(self, asset):
    return ' '.join([t.tag for t in asset.tags])

  def resolve_data_dumps(self, asset):
    return json.dumps(asset.data) if None != asset.data else ''


class SchemaSerializeAssets(SchemaSerializeTimes):
  id        = fields.Integer()
  name      = fields.String()
  code      = fields.String()
  type      = fields.String()
  location  = fields.String()
  status    = fields.String()
  condition = fields.String()
  data      = fields.Dict()
  notes     = fields.String()
  key       = fields.String()
  author_id = fields.Integer()
  
  # virtal
  tags       = fields.List(fields.String())
  docs       = fields.List(fields.Nested(SchemaSerializeDocs()))
  assets_has = fields.List(fields.Nested(lambda: SchemaSerializeAssets(exclude = ('assets_has',))))


class SchemaSerializeOrders(SchemaSerializeTimes):
  id     = fields.Integer()
  key    = fields.String()
  status = fields.String()
  data   = fields.Dict()
  notes  = fields.String()

  # foreign key
  site_id   = fields.Integer()
  
  # virtal
  site     = fields.Nested(SchemaSerializeAssets(exclude = ('assets_has',)))
  tags     = fields.List(fields.String())
  products = fields.List(fields.Nested(SchemaSerializeAssets(exclude = ('assets_has',))))


class ObjectIdField(fields.Field):
  def _serialize(self, value, attr, obj, **kwargs):
    if value is None:
      return None
    if isinstance(value, ObjectId):
      return str(value)
    if isinstance(value, str) and ObjectId.is_valid(value):
      # already a valid hex string; pass through
      return value
    raise ValidationError('Invalid ObjectId for serialization')

  def _deserialize(self, value, attr, data, **kwargs):
    if value is None:
      return None
    if isinstance(value, ObjectId):
      return value
    if isinstance(value, str) and ObjectId.is_valid(value):
      return ObjectId(value)
    raise ValidationError('Invalid ObjectId')
  
##SchemaMongoDoc
class SchemaMongoDoc(Schema):
  class Meta:
    # keep undeclared fields on load (optional)
    unknown = INCLUDE

  # expose Mongo '_id' as 'id'
  id = ObjectIdField(attribute = '_id', data_key = 'id', dump_only = True)

class SchemaMongoDocData(SchemaMongoDoc, SchemaSerializeTimes):
  data = fields.Dict()

