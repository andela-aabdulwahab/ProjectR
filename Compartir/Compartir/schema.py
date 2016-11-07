# using the django-graph-auth package https://github.com/morgante/django-graph-auth

from graphene import Schema
from graphene import relay, ObjectType

import graph_auth.schema

from links.schema import Query as LinkQuery


class Query(graph_auth.schema.Query, LinkQuery, ObjectType):
    node = relay.Node.Field()


class Mutation(graph_auth.schema.Mutation, ObjectType):
    pass

schema = Schema(query=Query, mutation=Mutation)
