'''
Dashdrum Django Snips

by Dan Gentry 

widgets.py
'''

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

