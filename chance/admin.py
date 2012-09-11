try:
    from reversion import VersionAdmin as ModelAdmin
except ImportError:
    from django.contrib.admin import ModelAdmin

from django.contrib import admin
from django.http import HttpResponse

from chance.models import (Event, EventFee, EventChoice, EventChoiceOption,
        Registration, EventChoiceSelection, Talk, Transaction)



class EventFeeInlineAdmin(admin.TabularInline):
    model = EventFee
    extra = 1

class EventChoiceInlineAdmin(admin.StackedInline):
    model = EventChoice
    extra = 1

class EventAdmin(ModelAdmin):
    date_hierarchy = 'starts'
    inlines = [
        EventFeeInlineAdmin,
        EventChoiceInlineAdmin
    ]


class EventChoiceOptionInlineAdmin(admin.TabularInline):
    model = EventChoiceOption
    extra = 1


class EventChoiceAdmin(ModelAdmin):
    inlines = [
        EventChoiceOptionInlineAdmin
    ]
    exclude = ('event',)
    actions = ['selection_summary']

    def selection_summary(self, request, queryset):
        response = HttpResponse(mimetype='text/plain')
        for choice in queryset.all():
            response.write('%s (%s)\n' % (choice.label, choice.event.name,))
            for option in choice.options.all():
                response.write('\t%s: %d\n' % (option.display,
                    EventChoiceSelection.objects.filter(option=option).count(),))
            response.write('\n')
        response.write('\n')
        return response
    selection_summary.short_description = u'Summary of user selections for ' \
            'a choice.'

class RegistrationAdmin(ModelAdmin):
    model = Registration
    exclude = ('event',)
    list_filter = ('event', 'paid',)
    actions = ['csv_summary']

    def csv_summary(self, request, queryset):
        import csv
        response = HttpResponse(mimetype='text/csv')
        writer = csv.writer(response)
        for registration in queryset.all():
            writer.writerow([registration.attendee_name,
                registration.attendee_email, unicode(registration.paid)])
        return response
    csv_summary.short_description = u'Get a CSV Summary'


class TalkAdmin(ModelAdmin):
    list_filter = ('event', 'accepted',)
    list_display = ('title','presenter','contact')

    def contact(self, obj):
        if obj.owner:
            name = obj.owner.get_full_name()
            if not name:
                name = obj.owner.email
            if not name:
                name = obj.owner.username
            if not name:
                name = str(obj.owner.pk)

            if obj.owner.email:
                return u'<a href="mailto:%s">%s</a>' % (obj.owner.email,
                        name,)
            return name
        return 'None'

    contact.short_description = u'Owner'
    contact.allow_tags = True

class TransactionAdmin(ModelAdmin):
    list_display = ('pk', 'owner', 'amount_paid', 'created', 'closed')

admin.site.register(Event, EventAdmin)
admin.site.register(EventChoice, EventChoiceAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Talk, TalkAdmin)
admin.site.register(Transaction, TransactionAdmin)

