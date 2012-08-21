from logging import getLogger

from django.conf import settings
from django.core.mail import send_mail, mail_managers
from django.db.models.signals import post_save
from django.template import Context
from django.template.loader import get_template, select_template

from chance.models import Registration, Transaction



log = getLogger('chance.signals')

def notify_attendee_of_registration(sender, instance, created, raw, **kwargs):
    if raw or not created:
        return
    context = Context({'object': instance})
    subject =  get_template('chance/registration_email_subject.txt').render(context)
    subject = ''.join(subject.splitlines())
    message = get_template('chance/registration_email.txt').render(context)

    send_mail(subject, message, getattr(settings, 'CHANCE_FROM_EMAIL',
        settings.SERVER_EMAIL), [instance.attendee_email])


def notify_managers_of_registration(sender, instance, created, raw, **kwargs):
    if raw or not created:
        return
    context = Context({'object': instance})
    subject = select_template([
        'chance/registration_email_manager_subject.txt',
        'chance/registration_email_subject.txt']).render(context)
    subject = ''.join(subject.splitlines())

    message = select_template([
        'chance/registration_email_manager.txt',
        'chance/registration_email.txt']).render(context)

    mail_managers(subject, message, getattr(settings, 'CHANCE_FROM_EMAIL',
        settings.SERVER_EMAIL))

def mark_transaction_registrations(sender, instance, created, raw, **kwargs):
    if raw:
        return

    if not instance.paid_in_full:
        log.error('Transaction not paid in full')
        log.error('%s paid of %s' % (repr(instance.amount_paid),
            repr(instance.total),))
        return

    for registration in instance.registrations.all():
        registration.paid = True
        registration.save()

if getattr(settings, 'CHANCE_NOTIFY_ATTENDEE_ON_REGISTRATION', True):
    post_save.connect(notify_attendee_of_registration, sender=Registration)

if getattr(settings, 'CHANCE_NOTIFY_MANAGERS_ON_REGISTRATION', True):
    post_save.connect(notify_managers_of_registration, sender=Registration)

if getattr(settings, 'CHANCE_UPDATE_REGISTRATION_ON_TRANSACTION', True):
    post_save.connect(mark_transaction_registrations, sender=Transaction)

