
import json

# https://marshmallow.readthedocs.io/en/stable/quickstart.html#field-validators-as-methods
from marshmallow import Schema
from marshmallow import fields


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

