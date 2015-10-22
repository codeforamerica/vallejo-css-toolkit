from django import forms

from workflow.models import CSSCall


class ReportForm(forms.ModelForm):

    class Meta:
        model = CSSCall

        fields = (
            'name',
            'address',
            'phone',
            'problem',
            'date',
            'resolution',
            'reported_datetime',
            'tags',
            'reporter_address_number',
            'reporter_street_name',
            'when_last_reported',
            'time_of_day_occurs',
            'num_people_involved',
            'safety_concerns',
            'reporter_alternate_contact'
        )
