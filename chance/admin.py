try:
    from reversion import VersionAdmin as ModelAdmin
except ImportError:
    from django.contrib.admin import ModelAdmin

from django.contrib import admin

from chance.models import (Event, EventFee, EventChoice, EventChoiceOption,
        Registration, EventChoiceSelection, Talk)



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

class RegistrationAdmin(ModelAdmin):
    model = Registration
    exclude = ('event',)
    list_filter = ('event', 'paid',)

class TalkAdmin(ModelAdmin):
    list_filter('event', 'accepted',)

admin.site.register(Event, EventAdmin)
admin.site.register(EventChoice, EventChoiceAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Talk, TalkAdmin)

