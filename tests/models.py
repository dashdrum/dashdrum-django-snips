from __future__ import unicode_literals
from django.db import models
from snips.models import ModelBase

class Author(ModelBase):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    
    def __unicode__(self):
        return self.name
    