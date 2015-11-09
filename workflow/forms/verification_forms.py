from django import forms
from django.template.defaultfilters import filesizeformat

from workflow.models import Verification
from vallejo_css_toolkit.settings import MAX_UPLOAD_SIZE


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
            'nlp_assigned',
            'code_contacted',
            'trespass_letter',
            'bank_name',
            'bank_contact',
            'bank_contact_phone'
        )


class RestrictedFileField(forms.FileField):

    def clean(self, *args, **kwargs):
        data = super(RestrictedFileField, self).clean(*args, **kwargs)
        try:
            if data.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError(('File size must be under %s. Current file size is %s.') % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(data.size)))
        except AttributeError:
            pass

        return data


class UploadAssetForm(forms.Form):
    uploaded_asset = RestrictedFileField(required=False)
