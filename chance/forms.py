from logging import getLogger

from django import forms
from django.forms.models import InlineForeignKeyField

from chance.models import Registration, Event, EventChoiceSelection



log = getLogger('chance.forms')

class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ('event', 'attendee_name', 'attendee_email',
                'fee_option')
    
    def __init__(self, *args, **kwargs):
        self.event_object = kwargs.pop('event')
        assert isinstance(self.event_object, Event)

        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.add_event_fields()
        self.fields['event'] = InlineForeignKeyField(self.event_object)

        if self.event_object.fee_options.count() > 0:
            self.fields['fee_option'].empty_label = None
            self.fields['fee_option'].required = True
        else:
            del self.fields['fee_option']

    
    def add_event_fields(self):
        for choice in self.event_object.choices.all():
            if choice.allow_multiple:
                field = forms.ModelMultipleChoiceField
                widget = forms.CheckboxSelectMultiple
            else:
                field = forms.ModelChoiceField
                widget = forms.Select

            self.fields[choice.name] = field(label=choice.label,
                    help_text=choice.description, required=choice.required,
                    queryset=choice.options.filter(enabled=True), widget=widget)

    def save(self, **kwargs):
        result = super(RegistrationForm, self).save()
        self.save_related()
        return result

    def save_related(self):
        selections = self.instance.selections

        for field in self.event_object.choices.all():
            if field.allow_multiple:
                field_selections = selections.filter(option__choice=field)
                current = set(s.option for s in field_selections)
                new = set(self.cleaned_data[field.name])
                field_selections.filter(option__in=list(current -
                    new)).delete()
                    
                for add in new - current:
                    EventChoiceSelection.objects.create(registration=self.instance,
                            option=add)
            else:
                if self.cleaned_data[field.name]:
                    current, created = self.instance.selections.get_or_create(
                        option__choice=field,
                        defaults={'option': self.cleaned_data[field.name]})
                    if current.option != self.cleaned_data[field.name]:
                        current.option = self.cleaned_data[field.name]
                else:
                    self.instance.selections.filter(option__choice=field).delete()



    

