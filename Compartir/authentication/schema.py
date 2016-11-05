from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphene import relay, AbstractType, Mutation, Node, Field, String, Boolean
from graphene_django.filter import DjangoFilterConnectionField


class UserNode(DjangoObjectType):

    class Meta:
        model = get_user_model()
        interfaces = (Node, )

    @classmethod
    def get_node(cls, id, context, info):
        user = super(UserNode, cls).get_node(id, context, info)
        if context.user and user == context.user:
            return user
        else:
            return None


class RegisterUser(relay.ClientIDMutation):
    ok = Boolean()
    user = Field(UserNode)

    class Input:
        username = String()
        email = String(required=True)
        password = String(required=True)
        first_name = String()
        last_name = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        model = get_user_model()

        email = input.pop('email')
        username = input.pop('username', email)
        password = input.pop('password')

        user = model.objects.create_user(username, email, password, **input)
        user.is_current_user = True

        return RegisterUser(ok=True, user=user)


class Query(AbstractType):
    user = Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)
    me = Field(UserNode)

    def resolve_me(self, args, context, info):
        return UserNode.get_node(context.user.id, context, info)


class Mutation(AbstractType):
    register_user = RegisterUser.Field()
