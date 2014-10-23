'''
Dashdrum Django Snips

by Dan Gentry 

fields.py
'''

##---------------------------------------------------------------------------##

from __future__ import unicode_literals
from django.forms import ChoiceField

''' Based on https://gist.github.com/davidbgk/651080 
    modified to mirror the functionality of ModelChoiceField '''
 
class EmptyChoiceField(ChoiceField):
    def __init__(self, choices=(), empty_label="---------", required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):
 
        # prepend an empty label unless the field is required AND
        # an initial value is supplied
        
        if required and (initial is not None):
            pass # don't prepend the empty label
        else:
            choices = tuple([(u'', empty_label)] + list(choices))
 
        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label,
                                        initial=initial, help_text=help_text, *args, **kwargs)
        
##---------------------------------------------------------------------------##
        