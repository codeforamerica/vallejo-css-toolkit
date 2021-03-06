from datetime import datetime

import pytz

from django import forms
from django.forms.widgets import Select

from workflow.models import CSSCall

TZ = pytz.timezone('America/Los_Angeles')


class ReportForm(forms.ModelForm):
    reported_date = forms.DateField()
    reported_time = forms.TimeField()

    class Meta:
        model = CSSCall

        fields = (
            'name',
            'address',
            'phone',
            'problem',
            'date',
            'resolution',
            'reported_date',
            'reported_time',
            'tags',
            'reporter_address_number',
            'reporter_street_name',
            'when_last_reported',
            'time_of_day_occurs',
            'num_people_involved',
            'safety_concerns',
            'reporter_alternate_contact',
            'address_number',
            'street_name',
            'source',
            'status',
            'report_type'
        )

    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop('readonly')
        super(ReportForm, self).__init__(*args, **kwargs)

        # self.fields['reporter_address_number'].widget = forms.TextInput(attrs={'placeholder': 'e.g.: 555'})
        self.fields['address_number'].widget = forms.TextInput(attrs={'placeholder': 'ex: 2'})

        self.fields['reporter_street_name'].widget = forms.TextInput(attrs={'placeholder': 'ex: 555 Santa Clara St'})
        self.fields['street_name'].widget = forms.TextInput(attrs={'placeholder': 'ex: Florida St'})

        self.fields['reported_date'].widget.format = '%m/%d/%Y'
        self.fields['reported_time'].widget.format = '%H:%M'

        # self.fields['name'].widget.attrs['readonly'] = True

        if 'instance' in kwargs and kwargs['instance'].reported_datetime:
            localized = kwargs['instance'].reported_datetime.astimezone(TZ)
            self.fields['reported_date'].initial = localized.date()
            self.fields['reported_time'].initial = localized.time()
        else:
            now = datetime.utcnow()
            now_tz = pytz.utc.localize(now).astimezone(TZ)
            self.fields['reported_date'].initial = now_tz.date()
            self.fields['reported_time'].initial = now_tz.time()

        if readonly:
            for field in self.fields:
                if isinstance(self.fields[field].widget, Select):
                    self.fields[field].widget.attrs['disabled'] = True
                else:
                    self.fields[field].widget.attrs['readonly'] = True

    def save(self, commit=True):
        model = super(ReportForm, self).save(commit=False)
        model.reported_datetime = datetime.combine(self.cleaned_data['reported_date'], self.cleaned_data['reported_time'])

        if commit:
            model.save()

        return model
