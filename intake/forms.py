from django import forms
from django.template.defaultfilters import filesizeformat

from vallejo_css_toolkit.settings import MAX_UPLOAD_SIZE


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
