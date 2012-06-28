from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import edit, detail

from chance.forms import RegistrationForm
from chance.models import Event, Registration



class RegistrationFormMixin(object):
    form_class = RegistrationForm
    model = Registration

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

    def form_valid(self, form):
        result = super(RegistrationFormMixin, self).form_valid(form)
        if self.request.user.is_authenticated():
            self.object.owner = self.request.user
            self.object.save()
        messages.info(self.request, 'Registration for %s saved' %
                (form.cleaned_data['attendee_name'],))
        return result

class CreateRegistrationView(RegistrationFormMixin, edit.CreateView):
    pass

class UpdateRegistrationView(RegistrationFormMixin, edit.UpdateView):
    pass

class DeleteRegistrationView(RegistrationFormMixin, edit.DeleteView):
    pass

class RegistrationDetailView(detail.DetailView):
    model = Registration

    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user.has_perm('chance.change_registration') \
            and not self.request.user == self.object.owner:
            return HttpResponseForbidden()
        return super(RegistrationDetailView, self).get(request, *args,
                **kwargs)

