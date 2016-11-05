from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphene import relay, AbstractType, Mutation, Node, Field
from graphene_django.filter import DjangoFilterConnectionField


class UserNode(DjangoObjectType):

    class Meta:
        model = get_user_model()
        interfaces = (Node, )

    @classmethod
    def get_node(cls, id, context, info):
        user = super(UserNode, cls).get_node(id, context, info)
        if context.user.id and user.id == context.user.id:
            return user
        else:
            return None


class Query(AbstractType):
    user = Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)
    me = Field(UserNode)

    def resolve_me(self, args, context, info):
        return UserNode.get_node(context.user.id, context, info)
