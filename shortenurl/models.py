import re

from django.db import models

# Create your models here.


class LinksManager(models.Manager):
    def get_active(self):
        return super(LinksManager, self).get_queryset().filter(active=True)


class Links(models.Model):
    """ Fields for Links model """

    main_url = models.URLField(unique=True)
    short_url = models.CharField(max_length=10, unique=True)
    active = models.BooleanField(default=True)

    objects = LinksManager()

    def __str__(self):
        return self.main_url
