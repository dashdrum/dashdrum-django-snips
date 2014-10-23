"""

Dashdrum Django Snips is distributed under the terms of the University 
of Illinois/NCSA Open Source License

Copyright (c) 2013 Dan Gentry 
All rights reserved.

Developed by:   Dan Gentry
                Dashdrum
                http://dashdrum.com
                
Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
with the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:

1) Redistributions of source code must retain the above copyright notice, this list 
of conditions and the following disclaimers.

2) Redistributions in binary form must reproduce the above copyright notice, this 
list of conditions and the following disclaimers in the documentation and/or other 
materials provided with the distribution.

3) Neither the names of Dan Gentry, Dashdrum , nor the names of its contributors 
may be used to endorse or promote products derived from this Software without 
specific prior written permission.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.

"""
try:
    from django.utils.timezone import now
except ImportError:
    from datetime.datetime import now

from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from snips.fields import EmptyChoiceField
from snips.forms import CustomErrorClassFormMixin, NoAsteriskTextErrorList

from .factories import AuthorFactory
from .models import Author
    
##---------------------------------------------------------------------------##
## Test EmptyChoiceField

class TestEmptyChoiceField(TestCase):

    def setUp(self):
        self.a1 = AuthorFactory.create()
        self.a2 = AuthorFactory.create()


    def test_no_choices(self):
        test_field = EmptyChoiceField(required=False)
        self.assertEqual(test_field.choices,[(u'',u"---------"),])

    def test_with_choices(self):
        test_field = EmptyChoiceField(choices=Author.objects.all(),required=False,initial=self.a1.pk)
        self.assertEqual(test_field.choices,[(u'',u"---------"),self.a1,self.a2])

    def test_required_initial(self):
        test_field = EmptyChoiceField(choices=Author.objects.all(),required=True,initial=self.a1.pk)
        self.assertNotEqual(test_field.choices[0],(u'',u"---------"))

    def test_required_no_initial(self):
        test_field = EmptyChoiceField(choices=Author.objects.all(),required=True)
        self.assertEqual(test_field.choices[0],(u'',u"---------"))

    def test_custom_label(self):
        test_field = EmptyChoiceField(choices=Author.objects.all(),empty_label=u'** None **',required=False)
        self.assertEqual(test_field.choices[0],(u'',u"** None **"))
    
##---------------------------------------------------------------------------##
## Test forms.CustomErrorClassFormMixin

class TestMixinNoErrorClass(CustomErrorClassFormMixin):
    pass

class TestMixinWithErrorClass(CustomErrorClassFormMixin):
    error_class = NoAsteriskTextErrorList

class TestCustomErrorClassFormMixin(TestCase):
    def test_error_class(self):
        ## Instantiate object with no error class
        
        self.assertRaises(ImproperlyConfigured,TestMixinNoErrorClass)
        
        ## Instantiate object with error class
        test_object = TestMixinWithErrorClass
        
        self.assertEqual(test_object.error_class,NoAsteriskTextErrorList)
    
##---------------------------------------------------------------------------##
## Test models.ModelBase

class TestModelBase(TestCase):

    def setUp(self):
        self.a1 = AuthorFactory.create()        

    def test_created_on(self):
        self.assertAlmostEqual(self.a1.created_on,now(),delta=timedelta(seconds=2))

    def test_updated_on(self):
        self.a1.age = 77
        self.a1.save()
        self.assertAlmostEqual(self.a1.updated_on,now(),delta=timedelta(seconds=2))
        self.assertNotEqual(self.a1.created_on, self.a1.updated_on)

    def test_allow_delete(self):
        self.assertTrue(self.a1.allow_delete)
    
##---------------------------------------------------------------------------##


