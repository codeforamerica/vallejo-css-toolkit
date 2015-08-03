from django import forms

from intake.models import Call


class CallForm(forms.ModelForm):

    class Meta:
        fields = (
            'id',
            'problem_description',
            'caller_name',
            'caller_number',
            'problem_address',
            'name_recording_url',
            'property_owner',
            'property_owner_phone',
            'assignee',
            'status'

        )

        model = Call
