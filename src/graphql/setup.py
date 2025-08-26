
import os

from flask import jsonify
from flask import request

from ariadne import graphql_sync
from ariadne import load_schema_from_path
from ariadne import make_executable_schema
from ariadne import QueryType
from ariadne import MutationType
# from ariadne import ObjectType


query    = QueryType()
mutation = MutationType()

import src.graphql.resolvers.query
import src.graphql.resolvers.mutation

type_defs = load_schema_from_path(os.path.join(
  os.path.dirname(__file__), 'schema.graphql'))

# schema = make_executable_schema(type_defs, query)
schema = make_executable_schema(type_defs, query, mutation)

def graphql_mount_endpoint(app):
  @app.route('/graphql', methods = ('POST',))
  def route_handle_graphql():
        
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
      schema,
      data,
      context_value = { 'request': request },
      debug = app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
