##-------------------- no_password -----------------------##
##                                                        ##
##  Sets up form in Admin that does not ask for password  ##
##  entry when adding or modifying a user record. Used    ##
##  when authentication is assumed to be external.        ##
##                                                        ##
##  Based on a page of the docs from django-authtools     ##
##                                                        ##
##  http://django-authtools.readthedocs.io/en/latest/     ##
##  how-to/invitation-email.html                          ##
##                                                        ##
##--------------------------------------------------------##

from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserCreationForm(UserCreationForm):
    """
    A UserCreationForm with optional password inputs.
    """

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2


class UserAdmin(UserAdmin):
    ''' Password fields are not included in fieldsets '''
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'description': (
                "Enter the new username and click save."
            ),
            'fields': ('username',),
        }),
    )

    def save_model(self, request, obj, form, change):
        ''' Will set an unusable password before save '''
        obj.set_unusable_password()
        super(UserAdmin, self).save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
