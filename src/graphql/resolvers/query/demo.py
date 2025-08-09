
from src.graphql.setup import query


@query.field('demo')
def resolve_demo(_o, _i):  
  # from flask_app       import db
  from src.models.docs import Docs

  dd = Docs.tagged('@vars')
  return Docs.dicts(dd)
  
  # return []
  # from firebase_admin import auth
  # from src.utils import Utils
  # from marshmallow import Schema
  # from marshmallow import fields

  # class SchemaUser(Schema):
  #   uid = fields.String(required = True)
  
  # r = Utils.ResponseStatus()

  # try:
  #   r.status = SchemaUser().dump(auth.get_user('HJnEKuILPvQ6BFkg4Lers4qqv243'))
    
  # except Exception as e:
  #   r.error = e
  
  # else:
  #   from src.services.jwt import JWT
  #   return { 'access_token': JWT.encode(r.status) }

  # return r.dump()
  
  # import base64
  # from flask import render_template
  # from src.services.pdf import printHtmlToPDF
  # return printHtmlToPDF(render_template('pdf/blank-a4.html', content = 'FOO:BAR'), 
  #                       base64_encoded = True)
  
  # from src.services.jwt import JWT
  # tok = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTIyMzMzLCJAIjoiMjAyNS0wOC0wMSAwOTozMjo0MS4zNjQ4MjUrMDA6MDAifQ.l4i5Q-1YRvSOTSp8_owJwDdQf5v3zmfASOWeQbe4-0I'
  # return JWT.encode({ 'admin@nikolav.rs': '122' })
