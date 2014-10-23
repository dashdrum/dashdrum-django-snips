'''
Dashdrum Django Snips

by Dan Gentry 

forms.py
'''

##---------------------------------------------------------------------------##
from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured
    
class CustomErrorClassViewMixin(object):
    
    ''' Will set the error_class attribute
        on the form with the provided value 
        found in the error_class variable 
        
        Usage:

            views.py:
    
            class MyViewName(CustomErrorClassViewMixin, [a FormMixin descendant, such as CreateView])
    
                error_class = MyCustomErrorListClass
                
    '''
    
    error_class = None
    
    def get_form_kwargs(self):
        # Make sure that the error_class attribute is set on the
        # view, or raise a configuration error.
        if self.error_class is None:
            raise ImproperlyConfigured("'CustomErrorClassViewMixin' requires "
                "'error_class' attribute to be set.")
    
        kwargs = super(CustomErrorClassViewMixin,self).get_form_kwargs()
    
        kwargs.update({'error_class': self.error_class})
    
        return kwargs