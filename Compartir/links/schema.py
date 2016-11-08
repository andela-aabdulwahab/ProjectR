from django.contrib.auth.middleware import get_user

from graphene import AbstractType, Field, Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from links.models import LinkModel


def get_user_jwt(request):
    ''' Get the user class.
    return the default user object from django if user is authenticated through
    session or basic. If not authenticate the user through
    JSONWebTokenAuthentication
    '''
    user = get_user(request)
    if not user.is_authenticated():
        user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            return user_jwt[0]
    return user


class LinkNode(DjangoObjectType):

    class Meta:
        model = LinkModel
        interfaces = (Node, )
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'],
        }


class Query(AbstractType):
    links = Field(LinkNode)
    all_links = DjangoFilterConnectionField(LinkNode)

    def resolve_all_links(self, args, context, info):

        # a user object from get_user_jwt
        user = get_user_jwt(context)
        if not user.is_authenticated():
            return LinkModel.objects.none()
        return LinkModel.objects.filter(owner=user)
