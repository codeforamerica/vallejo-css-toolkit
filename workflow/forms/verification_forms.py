from django import forms

from workflow.models import Verification


class PropertyDetailsForm(forms.ModelForm):

    class Meta:
        model = Verification

        fields = (
            'property_description',
            'owner_name',
            'owner_address',
            'owner_primary_contact',
            'owner_secondary_contact',
            'water_service',
            'pge_service',
            'boarded',
            'nlp_assigned'
        )
