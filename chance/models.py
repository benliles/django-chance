from decimal import Decimal

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models



def validate_choice_name(value):
    if value and value.lower() in ('name', 'location', 'starts', 'ends',
        'registration_limit'):
        raise ValidationError(u'%s is a reserved field name, please choose ' \
                'a different one')

class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    registration_limit = models.PositiveSmallIntegerField(null=True,
            blank=True, default=0)
    slug = models.SlugField(max_length=16, null=True, blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('chance:chance_event', (), {'pk': self.pk})

    @property
    def registration_open(self):
        return self.registration_limit == 0 or \
            self.registrations.count() < self.registration_limit

class EventFee(models.Model):
    event = models.ForeignKey(Event, related_name='fee_options')
    available = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=255,decimal_places=2)

    def __unicode__(self):
        return u'%s at %s' % (self.name, self.event.name,)

class EventChoice(models.Model):
    event = models.ForeignKey(Event, related_name='choices')
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=32,
            validators=[validate_choice_name])
    label = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    required = models.BooleanField(default=False)
    allow_multiple = models.BooleanField(default=False)

    class Meta:
        ordering = ('order',)
        unique_together = ('name', 'event',)


    def __unicode__(self):
        return '%s at %s' % (self.name, self.event.name,)

class EventChoiceOption(models.Model):
    choice = models.ForeignKey(EventChoice, related_name='options')
    order = models.PositiveIntegerField(default=0)
    display = models.CharField(max_length=128)
    enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.display

class Registration(models.Model):
    event = models.ForeignKey(Event, related_name='registrations')
    owner = models.ForeignKey(User, related_name='+', null=True, blank=True)
    attendee_name = models.CharField(max_length=255)
    attendee_email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True)
    fee_option = models.ForeignKey(EventFee, related_name='+', null=True,
            blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)

    def get_absolute_url(self):
        if self.event.slug:
            try:
                return reverse('chance:chance_registration_slug', (), {'pk':
                    self.pk, 'slug': self.event.slug})
            except:
                pass
        return reverse('chance:chance_registration', (), {'pk': self.pk, 'event':
            self.event.pk})

    def __unicode__(self):
        return u'Registration for %s by %s' % (self.event.name,
                self.attendee_name,)

class EventChoiceSelection(models.Model):
    registration = models.ForeignKey(Registration, related_name='selections')
    option = models.ForeignKey(EventChoiceOption, related_name='+')


class Talk(models.Model):
    event = models.ForeignKey(Event, related_name='+')
    title = models.CharField(max_length=255, db_index=True)
    presenter = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    accepted = models.NullBooleanField(default=None)
    owner = models.ForeignKey(User, related_name='+', null=True, blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('chance:talk', (), {'pk': self.pk, 'event': self.event.pk})

    class Meta:
        ordering = ('event', 'title',)


class Transaction(models.Model):
    owner = models.ForeignKey(User, related_name='+', null=True, blank=True)
    registrations = models.ManyToManyField(Registration, related_name='+')
    amount_paid = models.DecimalField(max_digits=8,decimal_places=2,
            default='0.00')
    created = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.pk)

    @models.permalink
    def get_absolute_url(self):
        return ('chance:transaction', (), {'pk':self.pk})

    @property
    def total(self):
        return sum([r.fee_option.amount for r
            in self.registrations.all()])

    @property
    def paid_in_full(self):
        return self.total == self.amount_paid

class Track(models.Model):
    event = models.ForeignKey(Event, related_name='tracks')
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return '%s at %s' % (self.name, unicode(self.event),)

class ScheduleItem(models.Model):
    track = models.ForeignKey(Track, related_name='items')
    talk = models.ForeignKey(Talk, related_name='+', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    @property
    def start_date(self):
        if self.start:
            return self.start.date()
        return None

    def __unicode__(self):
        if self.talk:
            return self.talk.title
        elif self.name:
            return self.name
        return unicode(self.pk)

    class Meta:
        ordering = ('start','track',)

try:
    import reversion

    reversion.register(EventChoiceOption)
    reversion.register(EventChoice, follow=['options'])
    reversion.register(EventFee)
    reversion.register(Event, follow=['fee_options', 'choices'])

    reversion.register(EventChoiceSelection)
    reversion.register(Registration, follow=['selections'])
    reversion.register(Talk)
    reversion.register(Transaction)
    reversion.register(Track, follow=['items'])
    reversion.register(ScheduleItem)
except ImportError:
    pass

