from datetime import datetime

from django import forms

from workflow.models import CSSCall


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
            'reporter_alternate_contact'
        )

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            self.fields['reported_date'].initial = kwargs['instance'].reported_datetime.date()
            self.fields['reported_time'].initial = kwargs['instance'].reported_datetime.time()

    def save(self, commit=True):
        model = super(ReportForm, self).save(commit=False)
        model.reported_datetime = datetime.combine(self.cleaned_data['reported_date'], self.cleaned_data['reported_time'])

        if commit:
            model.save()

        return model
