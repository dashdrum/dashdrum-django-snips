dashdrum-django-snips
=====================

A collection of code snippets that I use in my Django apps

## fields.py

### Empty Choice Field

Extends Django's ChoiceField to provide an empty label similar to a ModelChoiceField

* The empty_label parameter defaults to u"---------", but can be overridden
* A required field has the empty field choice prepended to the list, unless an initial value is provided.
* When the field is not required, the empty field choice is always included, regardless of whether an initial value exists

Based on [https://gist.github.com/davidbgk/651080](https://gist.github.com/davidbgk/651080)

Usage:

    in forms.py:
    
    class MyFormName(Form):
        
        suitability = EmptyChoiceField(required=False,choices=Suitability)
        
See this link for a full write-up with example:
    [http://dashdrum.com/blog/2013/02/django-emptychoicefield/](http://dashdrum.com/blog/2013/02/django-emptychoicefield/)

## forms.py

### CustomErrorClassFormMixin

This little mixin provides an easy way to declare a custom ErrorClass for a form

Usage:

	in forms.py:
	
	class MyFormName(CustomErrorClassFormMixin, ModelForm)
	
		error_class = MyCustomErrorListClass
	
Notes:

* The mixin must be declared before the form class in order to update the error_class in kwargs before the form's __init__() method fires
* The `error_class` attribute must be defined 
* See NoAsteriskTextErrorList as an example of a custom ErrorList


### NoAsteriskTextErrorList

A simple example of defining a custom ErrorList, this class changes the default rendering example to the as_text() method, 
and that method is slightly modified from the stock behavior to not include an asterisk before each error. 

Usage:

	in views.py
	
	form = MyFormName(data=form_data, error_class=NoAsteriskTextErrorList)
	
Or try the CustomErrorClassFormMixin or CustomErrorClassViewMixin

## models.py

### ModelBase

ModelBase extends the Model class and provides a couple of features I like to see in all of my models.

* The fields `created_on` and `updated_on` keep track of when the object is created or modified
* The `allow_delete` property can be overridden for each model to indicate when a delete is safe. Helps avoid accidental cascading deletes.

Usage:

    in models.py
    
    class MyModel(ModelBase):
        # define fields - created_on and updated_on are already defined
        
        @property
        def allow_delete(self):
        	if # some condition #:
        		return False
        	return True
        	
An example of a condition that could be used in the `allow_delete` function would be to check to see if there are any linked objects.

    if len(MyModel.objects.get(id=self.id).anothermodel_set.all()) == 0:  ## Check for linked objects
        return False  ## objects are linked
    return True ## OK to delete

## utils.py

### truncate_to_space(orig,max)

Truncates the given string to the desired length at the nearest available space.

Usage:

    short_name = truncate_to_space(full_name,10)
    
### is_valid_email(email)

Uses the Django provided regular expression to validate an email address.

Usage:

    if is_valid_email(email_field):
    	send_email(email_field)

### Choice

From [http://tomforb.es/using-python-metaclasses-to-make-awesome-django-model-field-choices?pid=0](http://tomforb.es/using-python-metaclasses-to-make-awesome-django-model-field-choices?pid=0)

A metaclass that makes for simple ModelField choices

Usage:

    in models.py (or wherever you wish):
    
    class ActionType(Choice):
        AWAITING_APPROVAL = 'E'
        APPROVED = 'A'
        REJECTED = 'R'
        IN_PROCESS = 'I'
        TO_COMMITTEE = 'C'
        NEEDS_RESEARCH = 'N'
        
    in forms.py:
    
    class MyFormName(Form):
        
        action_type = ChoiceField(required=False,choices=ActionType)	    

## views.py

### CustomErrorClassViewMixin

When used with a class based view descendent from FormMixin, this will include the custom error_class
value in the `get_form_kwargs` method.

    Usage:

        views.py:

        class MyViewName(CustomErrorClassViewMixin, [a FormMixin descendant, such as CreateView])

            error_class = MyCustomErrorListClass
	
Note:
* The `error_class` attribute must be defined
* See NoAsteriskTextErrorList as an example of a custom ErrorList

### FormsetMixin, FormsetCreateMixin, FormsetUpdateMixin

Set of mixins to add formset processing to class based views

FormsetMixin is the parent class that provides most of the functionality. However, the get() and post() methods need to be subclassed to provide a value for self.object.

FormsetCreateMixin and FormsetUpdateMixin both handle the assignment of self.object as is appropriate for their function.

Usage:
  
Use FormsetCreateMixin and FormsetUpdateMixin along with the corresponding class-based view.  Also, the instance variable detail\_form\_class should be defined.

Example:

    class MyView(FormsetCreateMixin, CreateView):
        model = MyModel
        form_class = MyModelForm
        detail_form_class = MyFormest
    
## widgets.py

### CustomRelatedFieldWidgetWrapper

Based on RelatedFieldWidgetWrapper, this version does the same thing outside of the admin interface.

See this link for a full write-up with example:

   [http://dashdrum.com/blog/2012/12/more-relatedfieldwidgetwrapper-the-popup/ ](http://dashdrum.com/blog/2012/12/more-relatedfieldwidgetwrapper-the-popup/ )
   

### SelectDisabled

Adds the ability to disable selected choices of a Select control
        
Usage:
        
    in forms.py:
        
    class MyForm(Form): 
        def __init__(self, disabled, *args, **kwargs):
            super(MyForm, self).__init__(*args, **kwargs)
            if disabled:
                self.fields['my_field'].widget.disabled = disabled
                    
        my_field = ModelChoiceField(widget=SelectDisabled(),queryset=MyModel.objects.all(),empty_label=None)  
            
    in views.py:
        
        ## Set a condition in the filter clause of the query to return 
        ## the disabled items
        
        disabled = []
        for m in MyModel.objects.filter(##condition##).values_list('id'):
            disabled.append(m[0])
                
        form = MyForm( data=request.POST or None, disabled=disabled)

