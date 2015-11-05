from django import forms
from django.template.defaultfilters import filesizeformat

from vallejo_css_toolkit.settings import MAX_UPLOAD_SIZE
from workflow.models import CSSCall


class RestrictedFileField(forms.FileField):

    def clean(self, *args, **kwargs):
        data = super(RestrictedFileField, self).clean(*args, **kwargs)
        try:
            print data.size
            if data.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError(('File size must be under %s. Current file size is %s.') % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(data.size)))
        except AttributeError:
            pass

        return data


class IntakeIssueForm(forms.Form):
    error_css_class = 'form-error'

    CHOICES = [
        ('yes', ' Yes'),
        ('no', ' No'),
        ('unsure', "I'm not sure")
    ]

    problem_location = forms.CharField()
    description = forms.CharField()
    how_many_people = forms.CharField(required=False)
    time_of_day = forms.CharField(required=False)
    how_long = forms.CharField(required=False)
    uploaded_photo = RestrictedFileField(required=False)
    safety_concerns = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=False)
    reported_before = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=False)
    reported_before_details = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(IntakeIssueForm, self).__init__(*args, **kwargs)

        self.fields['how_many_people'].widget = forms.TextInput(attrs={'placeholder': 'ex: 4'})
        self.fields['time_of_day'].widget = forms.TextInput(attrs={'placeholder': 'ex: night'})
        self.fields['how_long'].widget = forms.TextInput(attrs={'placeholder': 'ex: 3 days'})
        self.fields['reported_before_details'].widget = forms.TextInput(attrs={'placeholder': 'ex: yesterday, to Code Enforcement'})
        self.fields['problem_location'].widget = forms.TextInput(attrs={'placeholder': 'Address or cross street'})


class IntakeContactForm(forms.Form):
    error_css_class = 'form-error'

    CONTACT_METHOD_CHOICES = [
        (CSSCall.EMAIL_CONTACT_PREFERENCE, 'Email'),
        (CSSCall.TEXT_CONTACT_PREFERENCE, 'Text Message'),
        (CSSCall.NO_CONTACT_PREFERENCE, "I don't want to receive updates")
    ]

    reporter_name = forms.CharField(required=False)
    reporter_phone = forms.CharField(required=False)
    reporter_address = forms.CharField(required=False)
    reporter_email = forms.EmailField(required=False)
    reporter_contact_method = forms.ChoiceField(choices=CONTACT_METHOD_CHOICES, required=False)

    def clean(self, *args, **kwargs):
        data = super(IntakeContactForm, self).clean(*args, **kwargs)

        if not data.get('reporter_email') and data.get('reporter_contact_method') == 'email':
            raise forms.ValidationError('You chose to receive email updates but did not provide an email address.')

        if not data.get('reporter_phone') and data.get('reporter_contact_method') == 'text':
            raise forms.ValidationError('You chose to receive email updates but did not provide a phone number.')
