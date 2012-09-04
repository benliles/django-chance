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

class TalkAdmin(ModelAdmin):
    list_filter = ('event', 'accepted',)
    list_display = ('title','presenter','contact')

    def contact(self, obj):
        if obj.owner:
            if obj.owner.email:
                return u'<a href="mailto:%s">%s</a>' % (obj.owner.email,
                        obj.owner.get_full_name(),)
            return obj.owner.get_full_name()
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

