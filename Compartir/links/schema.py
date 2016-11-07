from graphene import AbstractType, Field, Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from links.models import LinkModel


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

        if not context.user.is_authenticated():
            return LinkModel.objects.none()
        else:
            return LinkModel.objects.filter(owner=context.user)
