
from marshmallow import Schema
from marshmallow import fields

class SchemaAuthArguments(Schema):
  uid = fields.String(required = True)

class SchemaValidateCloudMessagingMessage(Schema):
  title = fields.String(required = True)
  body  = fields.String(required = True)
  data  = fields.Dict(allow_none = True)

