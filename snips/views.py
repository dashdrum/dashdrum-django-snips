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

#-----------------------------------------------------------------------------#

class DoubleObjectMixin(object):

    def get_other_object(self, other_queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.other_queryset` and a `pk` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if other_queryset is None:
            other_queryset = self.get_other_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            other_queryset = other_queryset.filter(pk=pk)
        # If none of those are defined, it's an error.
        if pk is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            # Get the single item from the filtered queryset
            other_obj = other_queryset.get()
        except other_queryset.model.DoesNotExist: # Allow record to be not found
            other_obj = None
        return other_obj

    def get_other_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        Note that this method is called by the default implementation of
        `get_object` and may not be called if `get_object` is overridden.
        """
        if self.other_queryset is None:
            if self.other_model:
                return self.other_model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.other_model, %(cls)s.other_queryset, or override "
                    "%(cls)s.get_other_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.other_queryset.all()

class OneToOneMixin(DoubleObjectMixin):

    ''' Mixin to support processing of a parent record and a one-to-one related
        child record.

        Expects self.other_object to be set by downstream methods
        in get() and post() '''

    other_model=None
    other_form_class = None
    other_queryset = None
    other_object = None
    other_fields = None

    def get(self, request, *args, **kwargs):
        ## Expects self.other_object to be set by a downstream method ##
        return super(OneToOneMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """

        ## Expects self.object and self.other_object to be set by a downstream method ##

        form = self.get_form()
        other_form = self.get_other_form()
        if all((form.is_valid(), other_form.is_valid())):
            return self.form_valid(form,other_form)
        else:
            return self.form_invalid(form,other_form)

    def form_valid(self, form, other_form):
        """
        If the forms are valid, save the associated model.
        """

        self.object = form.save()

        ## Set pointer to master record and save the other object
        self.other_object = other_form.save(commit=False)
        self.other_object.pk = self.object.pk
        self.other_object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, other_form):
        """
        If either form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return super(OneToOneMixin, self).form_invalid(form)

    def get_other_form(self, other_form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if other_form_class is None:
            other_form_class = self.get_other_form_class()
        return other_form_class(**self.get_other_form_kwargs())

    def get_other_form_class(self):
        """
        Returns the form class to use in this view.
        """
        if self.other_fields is not None and self.other_form_class:
            raise ImproperlyConfigured(
                "Specifying both 'other_fields' and 'other_form_class' is not permitted."
            )
        if self.other_form_class:
            return self.other_form_class
        else:
            if self.other_model is not None:
                # If a model has been explicitly provided, use it
                other_model = self.other_model
            elif hasattr(self, 'other_object') and self.other_object is not None:
                # If this view is operating on a single object, use
                # the class of that object
                other_model = self.other_object.__class__
            if self.other_fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'other_fields' attribute is prohibited." % self.__class__.__name__
                )
            return model_forms.modelform_factory(other_model, fields=self.other_fields)

    def get_other_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """

        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if hasattr(self, 'other_object'):
            kwargs.update({'instance': self.other_object})
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Insert the other form into the context dict.
        """
        kwargs.setdefault('other_form', self.get_other_form())

        """
        Insert the other single object into the context dict.
        """
        context = {}
        if self.other_object:
            context['other_object'] = self.other_object
            # context_other_object_name = self.get_context_object_name(self.other_object)
            # if context_other_object_name:
            #   context[context_other_object_name] = self.other_object
        context.update(kwargs)

        return super(OneToOneMixin, self).get_context_data(**context)

class OneToOneCreateMixin(OneToOneMixin):

    def get(self, request, *args, **kwargs):
        """
        Set self.other_object to None
        """
        self.other_object = None
        return super(OneToOneCreateMixin,self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Set self.object and self.other_object to None
        """
        self.object = None
        self.other_object = None
        return super(OneToOneCreateMixin,self).post(request, *args, **kwargs)

class OneToOneUpdateMixin(OneToOneMixin):

    def get(self, request, *args, **kwargs):
        """
        Get self.other_object
        """
        self.object = None
        self.other_object = self.get_other_object()
        return super(OneToOneUpdateMixin,self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Get self.object and self.other_object
        """
        self.object = self.get_object()
        self.other_object = self.get_other_object()
        return super(OneToOneUpdateMixin,self).post(request, *args, **kwargs)

class OneToOneDeleteMixin(DoubleObjectMixin):

    other_model=None
    other_queryset = None
    other_object = None

    def delete(self, request, *args, **kwargs):
        """
        Delete other_object, then pass upstream
        """

        self.other_object = self.get_other_object()
        if self.other_object:
            self.other_object.delete()
        return super(OneToOneDeleteMixin,self).delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Get self.other_object
        """
        self.object = None
        self.other_object = self.get_other_object()
        return super(OneToOneDeleteMixin,self).get(request, *args, **kwargs)
