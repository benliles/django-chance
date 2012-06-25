from django.shortcuts import get_object_or_404
from django.views.generic import edit

from chance.models import Event, Registration
from chance.forms import RegistrationForm



class RegistrationFormMixin(object):
    form_class = RegistrationForm
    model = Registration
    success_url = '/'

    def get(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs.get('event', None))
        del kwargs['event']
        return super(RegistrationFormMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs.get('event', None))
        del kwargs['event']
        return super(RegistrationFormMixin, self).post(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super(RegistrationFormMixin, self).get_form_kwargs()
        kwargs['event'] = self.event
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs = super(RegistrationFormMixin, self).get_context_data(**kwargs)
        kwargs['event'] = self.event
        return kwargs

class CreateRegistrationView(RegistrationFormMixin, edit.CreateView):
    pass

class UpdateRegistrationView(RegistrationFormMixin, edit.UpdateView):
    pass

