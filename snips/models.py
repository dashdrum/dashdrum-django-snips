from __future__ import unicode_literals

from django.db import models
from datetime import datetime 
try:
    from django.utils.timezone import now
except ImportError:
    from datetime.datetime import now
from django.utils.translation import ugettext_lazy as _


class ModelBase(models.Model):
    """
    Abstract base class for all models.  Adds timestamp fields.
    """
    created_on = models.DateTimeField(_('created on'), default=now, editable=False, )
    updated_on = models.DateTimeField(_('updated on'), editable=False)
    
    @property
    def allow_delete(self):
        """ 
        default behavior for allow_delete property  
        models can override 
        """
        return True
  
    class Meta:
        abstract = True
 
    def save(self,*args, **kwargs):
        self.updated_on = now()
        super(ModelBase, self).save(*args, **kwargs)
        
#
#----------------------
        