from django.db import models



class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    registration_limit = models.PositiveSmallIntegerField(null=True,
            blank=True, default=0)

    def __unicode__(self):
        return self.name

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
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    required = models.BooleanField(default=False)
    allow_multiple = models.BooleanField(default=False)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return '%s at %s' % (self.name, self.event.name,)

class EventChoiceOption(models.Model):
    choice = models.ForeignKey(EventChoice, related_name='options')
    order = models.PositiveIntegerField(default=0)
    value = models.CharField(max_length=32)
    display = models.CharField(max_length=128)
    enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ('order',)

class Registration(models.Model):
    event = models.ForeignKey(Event, related_name='registrations')
    attendee_name = models.CharField(max_length=255)
    attendee_email = models.EmailField()
    fee_option = models.ForeignKey(EventFee, related_name='+', null=True,
            blank=True)
    paid = models.BooleanField(default=False)

class EventChoiceSelection(models.Model):
    registration = models.ForeignKey(Registration, related_name='selections')
    option = models.ForeignKey(EventChoiceOption, related_name='+')


try:
    import reversion
    
    reversion.register(EventChoiceOption)
    reversion.register(EventChoice, follow=['options'])
    reversion.register(EventFee)
    reversion.register(Event, follow=['fee_options', 'choices',
        'choices__options'])

    reversion.register(EventChoiceSelection)
    reversion.register(Registration, follow=['selections'])
except ImportError:
    pass

