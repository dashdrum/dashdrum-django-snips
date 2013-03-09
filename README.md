dashdrum-django-snips
=====================

A collection of code snippets that I use in my Django apps

# Just starting out

Before I get much documentation here, I need to get my house in order - meaning I need to organize the code.  Watch this space for descriptions of each reusable snippet as I work through the list.

## widgets.py

### CustomRelatedFieldWidgetWrapper

Based on RelatedFieldWidgetWrapper, this version does the same thing outside of the admin interface.

See this link for a full write-up with example:

   [http://dashdrum.com/blog/2012/12/more-relatedfieldwidgetwrapper-the-popup/ ](http://dashdrum.com/blog/2012/12/more-relatedfieldwidgetwrapper-the-popup/ )
   

### SelectDisabled

Adds the ability to disable selected options of a Select control

## forms.py

### CustomErrorClassMixin

This little mixin provides an easy way to declare a custom ErrorClass for a form

Usage:

	in forms.py:
	
	class MyFormName(CustomErrorClassMixin, ModelForm)
	
		error_class = MyCustomErrorListClass
	
Notes:
* The mixin must be declared before the form class in order to update the error_class in kwargs before the form's __init__() method fires
* The `error_class` attribute must be defined


### NoAsteriskTextErrorList

A simple example of defining a custom ErrorList, this class changes the default rendering example to the as_text() method, 
and that method is slightly modified from the stock behavior to not include an asterisk before each error. 

Usage:

	in views.py
	
	form = MyFormName(data=form_data, error_class=NoAsteriskTextErrorList)
	
Or try the CustomErrorClassMixin
	

