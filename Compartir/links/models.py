from django.db import models

# Create your models here.


class LinkModel(models.Model):

    url = models.URLField(max_length=300)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    # consider the django tag model to add tags
