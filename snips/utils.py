'''
Created on Sep 1, 2010

@author: dgentry
'''

def truncate_to_space(orig,max):
    """
    Truncates a string to the desired length at the closest space
    
    orig - source string to be truncated
    max  - desired max length of truncated result
    
    Doctests:
    
    >>> truncate_to_space('Dan Gentry',7) 
    'Dan'
    
    >>> truncate_to_space('Dan Gentry',15)
    'Dan Gentry'
    
    >>> truncate_to_space('Dan Gentry',10)
    'Dan Gentry'
    
    >>> truncate_to_space('Dan Gentry',1)
    'D'
    
    >>> truncate_to_space('Dan Gentry',0)
    ''
    
    This next one has 51 z characters as input, and should output 50 of them
    >>> truncate_to_space('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',50)
    'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
    
    Here is an x, followed by a space and 51 z characters
    >>> truncate_to_space('x zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',50)
    'x'
    
    >>> truncate_to_space('What is Translational Research? The Purdue University-Indiana University Partnership that built the Indiana Clinical and Translational Sciences Institute',50)
    'What is Translational Research? The Purdue'
    
    """

    if len(orig) <= max: ## already shorter or equal to max length
        return orig
        
    for i in range(max,0,-1):
        if orig[i] == " ":  ## found a space
            return orig[:i] ## Return portion before the found space
        
    return orig[:max]  ## Couldn't find a space. Truncate to max length

#-----------------------------------------------------------------------------#
#

## Validate email address
from django.core.validators import email_re

def is_valid_email(email):
    return True if email_re.match(email) else False

#-----------------------------------------------------------------------------#
#  Choice metaclass from http://tomforb.es/using-python-metaclasses-to-make-awesome-django-model-field-choices?pid=0
#

import inspect

class Choice(object):
    class __metaclass__(type):
        def __init__(self, *args, **kwargs):
            self._data = []
            for name, value in inspect.getmembers(self):
                if not name.startswith('_') and not inspect.ismethod(value):
                    if isinstance(value, tuple) and len(value) > 1:
                        data = value
                    else:
                        pieces = [x.capitalize() for x in name.split('_')]
                        data = (value, ' '.join(pieces))
                    self._data.append(data)
                    setattr(self, name, data[0])

            self._hash = dict(self._data)

        def __iter__(self):
            for value, data in self._data:
                yield (value, data)

    @classmethod
    def get_value(self, key):
        return self._hash[key]
#
#-----------------------------------------------------------------------------#    
