from decimal import Decimal
from logging import getLogger
from urllib2 import urlopen

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.db.models import permalink
from django.http import (HttpResponseForbidden, HttpResponseRedirect, 
                         HttpResponse, Http404, HttpResponseBadRequest)
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.simplejson import load
from django.views import generic

from chance.forms import (RegistrationForm, TalkSubmissionForm,
                            TransactionConfirmForm)
from chance.models import Event, Registration, Talk, Transaction



log = getLogger('chance.views')

class EventMixin(object):
    def get(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs.get('event', None))
        del kwargs['event']
        return super(EventMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs.get('event', None))
        del kwargs['event']
        return super(EventMixin, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(EventMixin, self).get_context_data(**kwargs)
        kwargs['event'] = self.event
        return kwargs


class EventRelatedFormMixin(EventMixin):
    def get_form_kwargs(self):
        kwargs = super(EventRelatedFormMixin, self).get_form_kwargs()
        kwargs['event'] = self.event
        return kwargs

class RegistrationFormMixin(EventRelatedFormMixin):
    form_class = RegistrationForm
    model = Registration

    def form_valid(self, form):
        result = super(RegistrationFormMixin, self).form_valid(form)
        if self.request.user.is_authenticated():
            self.object.owner = self.request.user
            self.object.save()
        messages.info(self.request, 'Registration for %s saved' %
                (form.cleaned_data['attendee_name'],))
        return result

class CreateRegistrationView(RegistrationFormMixin, generic.CreateView):
    def get(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs.get('event', None))
        if not self.event.registration_open:
            messages.error(request, u'%s registration is no longer available' %
                    (self.event.name,))
            return HttpResponseRedirect(self.event.get_absolute_url())
        return super(CreateRegistrationView, self).get(request, *args,
                **kwargs)

    def post(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs.get('event', None))
        if not self.event.registration_open:
            messages.error(request, u'%s registration is no longer available' %
                    (self.event.name,))
            return HttpResponseRedirect(self.event.get_absolute_url())
        return super(CreateRegistrationView, self).post(request, *args,
                **kwargs)

class UpdateRegistrationView(RegistrationFormMixin, generic.UpdateView):
    pass

class DeleteRegistrationView(RegistrationFormMixin, generic.DeleteView):
    def can_delete(self):
        return not self.object.paid

    def get(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.object = self.get_object()
        if not self.can_delete():
            messages.error(request, u'This registration cannot be canceled')
            return HttpResponseRedirect(self.object.get_absolute_url())
        return super(DeleteRegistrationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.object = self.get_object()
        if not self.can_delete():
            messages.error(request, u'This registration cannot be canceled')
            return HttpResponseRedirect(self.object.get_absolute_url())
        return super(DeleteRegistrationView, self).post(request, *args, **kwargs)


    @permalink
    def get_success_url(self):
        return ('chance_event', (), {'pk': self.object.event.pk},)

class RegistrationDetailView(EventMixin, generic.DetailView):
    model = Registration

    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user.has_perm('chance.change_registration') \
            and not self.request.user == self.object.owner:
            return HttpResponseForbidden()
        return super(RegistrationDetailView, self).get(request, *args,
                **kwargs)

class RegistrationListView(EventMixin, generic.ListView):
    model = Registration

    def get_queryset(self):
        qs = Registration.objects.filter(event=self.event)

        if self.request.user.has_perm('chance.change_registration'):
            return qs
        if self.request.user.is_authenticated():
            return qs.filter(owner=self.request.user)
        return qs.none()

class TalkListView(EventMixin, generic.ListView):
    model = Talk

class TalkDetailView(EventMixin, generic.DetailView):
    model = Talk

class TalkSubmissionCreateView(EventRelatedFormMixin, generic.CreateView):
    model = Talk
    form_class = TalkSubmissionForm

    def form_valid(self, form):
        result = super(TalkSubmissionCreateView, self).form_valid(form)
        if self.request.user.is_authenticated():
            self.object.owner = self.request.user
            self.object.save()
        messages.info(self.request, 'Talk submitted.')
        return result

class TalkSubmissionUpdateView(EventRelatedFormMixin, generic.UpdateView):
    model = Talk
    form_class = TalkSubmissionForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user.has_perm('change.change_talk') \
            and not self.request.user == self.object.owner:
                return HttpResponseForbidden()
        return super(TalkSubmissionUpdateView, self).get(request, *args,
                **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user.has_perm('change.change_talk') \
            and not self.request.user == self.object.owner:
                return HttpResponseForbidden()
        return super(TalkSubmissionUpdateView, self).post(request, *args,
                **kwargs)

        def form_valid(self, form):
            result = super(TalkSubmissionUpdateView, self).form_valid(form)
            messages.info(self.request, 'Talk updated.')
            return result

class TransactionConfirmView(generic.CreateView):
    models = Transaction
    form_class = TransactionConfirmForm
    template_name = 'chance/transaction_confirm.html'

    def get_registrations(self, request):
        return Registration.objects.filter(owner=request.user, paid=False)

    def get_form_kwargs(self):
        kwargs = super(TransactionConfirmView, self).get_form_kwargs()
        kwargs['registrations'] = self.registrations
        return kwargs

    def form_valid(self, form):
        response = super(TransactionConfirmView, self).form_valid(form)
        self.object.owner = self.request.user
        self.object.save()
        return response

    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        registrations = self.get_registrations(request)
        if registrations.count() == 1:
            self.object = Transaction.objects.create(owner=request.user)
            self.object.registrations.add(registrations[0])
            return HttpResponseRedirect(self.get_success_url())
        if registrations.count() == 0:
            raise Http404('No unpaid registrations found')
        self.registrations = registrations
        return super(TransactionConfirmView, self).get(request, *args,
                **kwargs)

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        self.registrations = self.get_registrations(request)
        return super(TransactionConfirmView, self).post(self, request, *args,
                **kwargs)

class TransactionView(generic.DetailView):
    model = Transaction

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        response = super(TransactionView, self).get(request, *args, **kwargs)

        if not (request.user.pk == self.object.owner.pk or
                request.user.has_perm('chance.change_transaction')):
            raise Http404()
        return response

    def get_context_data(self, **kwargs):
        context = super(TransactionView, self).get_context_data(**kwargs)
        context['total'] = reduce(lambda x,y: x+y, [r.fee_option.amount for r
            in self.object.registrations.all()])
        context['payment_url'] = settings.PAYMENT_POST_URL
        context['payment_params'] = getattr(settings, 'PAYMENT_PARAMS', {})
        context['payment_amount_field'] = settings.PAYMENT_AMOUNT_FIELD
        context['payment_transaction_id_field'] = \
            settings.PAYMENT_TRANSACTION_ID_FIELD
        return context

class TransactionNotifyView(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        transaction = get_object_or_404(Transaction, pk=request.POST.get('transaction_id'))
        url = settings.PAYMENT_VERIFICATION_URL % transaction.__dict__
        try:
            connection = urlopen(url)
            data = load(connection)
            connection.close()
            assert unicode(transaction.id) == data.get('id',False)
            transaction.closed = data.get('success','0') != '0'
            transaction.amount_paid = data.get('amount','0')
            transaction.save()
        except:
            log.exception('Error getting transaction details')
            return HttpResponseBadRequest('Error getting transaction details')
        return HttpResponse('k thanks bye!')

