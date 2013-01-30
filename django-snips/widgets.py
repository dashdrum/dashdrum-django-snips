'''
Dashdrum Django Snips

by Dan Gentry 

widgets.py
'''

##====================================================================================##


from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext as _

class CustomRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
   
    """
        Based on RelatedFieldWidgetWrapper, this does the same thing
        outside of the admin interface
        
        the parameters for a relation and the admin site are replaced
        by a url for the add operation
        
        See this post for a full write up with instructions:
        
        http://dashdrum.com/blog/2012/12/more-relatedfieldwidgetwrapper-the-popup/ 
        
        Example:
        
        in forms.py
        
        class MyForm(ModelForm):
        
            my_field = ModelMultipleChoiceField(queryset=None,
                                                required=False)
                                                
            def __init__(self, *args, **kwargs):
                super(MyForm,self).__init__(*args, **kwargs)
                # set the widget with wrapper
                self.fields['my_field'].widget = CustomRelatedFieldWidgetWrapper(
                                                        FilteredSelectMultiple(('My Model Name'),False,),
                                                        reverse('url_name'),
                                                        True)
                self.fields['my_field'].queryset = MyModel.objects.all() 
                
            class Media:
                ## media for the FilteredSelectMultiple widget
                css = {
                    'all':(ADMIN_MEDIA_PREFIX + 'css/widgets.css',),
                }
                # jsi18n is required by the widget
                js = ( ADMIN_MEDIA_PREFIX + 'js/admin/RelatedObjectLookups.js',)
    """

    def __init__(self, widget, add_url,permission=True):
        self.is_hidden = widget.is_hidden
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.widget = widget
        self.add_url = add_url
        self.permission = permission

    def render(self, name, value, *args, **kwargs):
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        if self.permission:
            output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
                (self.add_url, name))
            output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))
        return mark_safe(u''.join(output))

##====================================================================================##

from django.forms.widgets import Select, force_unicode, flatatt, escape, mark_safe, chain, conditional_escape

class SelectDisabled(Select):
    
    """
        Disables specific items in a select control
        
        Example:
        
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
            
    """
    
    
    def __init__(self, attrs=None, choices=(), disabled=[]):
        super(SelectDisabled, self).__init__(attrs, choices)
        self.disabled = list(disabled)

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value], self.disabled)
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe(u'\n'.join(output))

    def render_options(self, choices, selected_choices, disabled_choices):
        def render_option(option_value, option_label):
            option_value = force_unicode(option_value)
            ## This next line adds a mesasge after the label for the option.  Modify as needed ##
            option_label = (option_value in disabled_choices) and (force_unicode(option_label) + ' - SOLD OUT') or force_unicode(option_label)
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            disabled_html = (option_value in disabled_choices) and u' disabled="disabled"' or ''
            return u'<option value="%s"%s%s>%s</option>' % (
                escape(option_value), selected_html, disabled_html,
                conditional_escape(option_label))
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        disabled_choices = set([force_unicode(v) for v in disabled_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(render_option(*option))
                output.append(u'</optgroup>')
            else:
                output.append(render_option(option_value, option_label))
        return u'\n'.join(output)


##====================================================================================##