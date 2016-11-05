import graphene
from graphene import relay, ObjectType

import graph_auth.schema


class Query(graph_auth.schema.Query, ObjectType):
    node = relay.Node.Field()


class Mutation(graph_auth.schema.Mutation, ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
