from django.contrib.auth.middleware import get_user

from graphene import AbstractType, Field, Node, relay, String, Boolean
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from links.models import LinkModel


def get_user_jwt(request):
    ''' Get the user class.
    return the default user object from django if user is authenticated through
    session or basic. If not authenticate the user through jwt with
    JSONWebTokenAuthentication
    '''
    user = get_user(request)
    if not user.is_authenticated():
        user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            return user_jwt[0]
    return user


def get_authenticated_user(request):
    user = get_user_jwt(request)
    if not user.is_authenticated():
        raise Exception("Action not allowed for Login User")
    return user


class LinkNode(DjangoObjectType):

    class Meta:
        model = LinkModel
        interfaces = (Node, )
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'],
        }
    pk = String()

    def resolve_pk(self, args, context, info):
        return self.id


class AddLink(relay.ClientIDMutation):

    class Input:
        title = String()
        url = String(required=True)
        description = String()

    ok = Boolean()
    link = Field(LinkNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        title = input.pop('title')
        url = input.pop('url')
        user = get_authenticated_user(context)
        link = LinkModel.objects.create(title=title, url=url,
                                        owner=user, **input)
        return AddLink(ok=True, link=link)


class UpdateLink(relay.ClientIDMutation):

    class Input:
        pk = String(required=True)
        title = String()
        url = String()
        description = String()

    ok = Boolean()
    link = Field(LinkNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        pk = input.pop('pk')
        user = get_authenticated_user(context)
        link = LinkModel.objects.get(pk=pk)

        if not link:
            raise Exception("Link not found")

        for key, value in input.items():
            setattr(link, key, value)

        link.save()
        return UpdateLink(ok=True, link=link)


class Query(AbstractType):
    links = Field(LinkNode)
    all_links = DjangoFilterConnectionField(LinkNode)

    def resolve_all_links(self, args, context, info):

        # a user object from get_user_jwt
        user = get_user_jwt(context)
        if not user.is_authenticated():
            return LinkModel.objects.none()
        return LinkModel.objects.filter(owner=user)


class Mutation(AbstractType):
    add_link = AddLink.Field()
    update_link = UpdateLink.Field()
