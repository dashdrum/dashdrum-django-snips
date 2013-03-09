'''
Dashdrum Django Snips

by Dan Gentry 

forms.py
'''

##---------------------------------------------------------------------------##

from django.utils.encoding import force_unicode
from django.forms.util import ErrorList
    
class NoAsteriskTextErrorList(ErrorList):
    ''' An ErrorList that defaults to the as_text() representation
        Also, the asterisk is removed from that method. '''
    
    def __unicode__(self):
        return self.as_text()

    def as_text(self):
        if not self: return u''
        return u'\n'.join([u' %s' % force_unicode(e) for e in self])
    
##---------------------------------------------------------------------------##

from django.core.exceptions import ImproperlyConfigured
    
class CustomErrorClassMixin(object):
    ''' Allows the declaration of a custom error_class for a form
    
        Requires the error_class attribute to be provided 
        
        Usage:

            forms.py:
    
            class MyFormName(CustomErrorClassMixin, ModelForm)
    
                error_class = MyCustomErrorListClass
    
        '''
    
    error_class = None ## Default to none
    
    def __init__(self, *args, **kwargs):
        # Make sure that the error_class attribute is set on the
        # form, or raise a configuration error.
        if self.error_class is None:
            raise ImproperlyConfigured("'CustomErrorClassMixin' requires "
                "'error_class' attribute to be set.")
            
        ## Set the error_class attribute
        kwargs['error_class'] = self.error_class
        
        ## Call the parent method
        super(CustomErrorClassMixin, self).__init__(*args, **kwargs)
    
##---------------------------------------------------------------------------##
        
        