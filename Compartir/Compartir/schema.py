import graphene
from graphene import relay, ObjectType

import authentication.schema


class Query(authentication.schema.Query, ObjectType):
    node = relay.Node.Field()


class Mutation(authentication.schema.Mutation, ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
