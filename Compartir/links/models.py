from django.db import models

# Create your models here.


class LinkModel(models.Model):

    url = models.URLField(max_length=300)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='links')
    # consider the django tag model to add tags

    def __str__(self):
        return self.title
