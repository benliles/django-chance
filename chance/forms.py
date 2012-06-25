from logging import getLogger

from django import forms

from chance.models import Registration, Event



log = getLogger('chance.forms')

class RegistrationForm(forms.ModelForm):
    model = Registration
    fields = ('event', 'attendee_name', 'attendee_email',
            'fee_option')
    
    def __init__(self, *args, **kwargs):
        self.event_object = kwargs.pop('event')
        assert isinstance(event, Event)

        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.add_event_fields()
        self.fields['event'] = forms.InlineForeignKeyField(self.event_object)

    
    def add_event_fields(self):
        for choice in self.event_object.choices.all():
            if choice.allow_multiple:
                field = forms.ModelMultipleChoiceField
            else:
                field = forms.ModelChoiceField

            self.fields[choice.name] = field(label=choice.label,
                    help_text=choice.description, required=choice.required,
                    queryset=choice.options.filter(enabled=True))

    def save(self, **kwargs):
        super(RegistrationForm, self).save()
        self.save_related()

    def save_related(self):
        selection = self.instance.selections

        for field in self.event_objects.choices.all():
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
                    create, current = self.instance.selections.get_or_create(
                        option__choice=field,
                        defaults={'option': self.cleaned_data[field.name]})
                    if current.option != self.cleaned_data[field.name]:
                        current.option = self.cleaned_data[field.name]
                else:
                    self.instance.selections.filter(option__choice=field).delete()



    

