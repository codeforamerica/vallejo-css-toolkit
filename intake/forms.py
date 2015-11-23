# -*- coding: utf-8 -*-

from django import forms
from django.template.defaultfilters import filesizeformat

from vallejo_css_toolkit.settings import MAX_UPLOAD_SIZE
from workflow.models import CSSCall


class RestrictedFileField(forms.FileField):

    def clean(self, *args, **kwargs):
        data = super(RestrictedFileField, self).clean(*args, **kwargs)
        try:
            if data.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError(('File size must be under %s. Current file size is %s.') % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(data.size)))
        except AttributeError:
            pass

        return data


class IntakeIssueForm(forms.Form):
    error_css_class = 'form-error'
    YES = 'Yes'
    NO = 'No'
    UNSURE = 'Unsure'

    EN_CHOICES = [
        (YES, ' Yes'),
        (NO, ' No'),
        (UNSURE, "I'm not sure")
    ]

    ES_CHOICES = [
        (YES, u' Sí'.encode('utf-8')),
        (NO, ' No'),
        (UNSURE, u' No sé'.encode('utf-8'))
    ]

    problem_location = forms.CharField()
    description = forms.CharField()
    how_many_people = forms.CharField(required=False)
    time_of_day = forms.CharField(required=False)
    how_long = forms.CharField(required=False)
    uploaded_photo = RestrictedFileField(required=False)
    safety_concerns = forms.ChoiceField(widget=forms.RadioSelect(), required=False)
    reported_before = forms.ChoiceField(widget=forms.RadioSelect(), required=False)
    reported_before_details = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        lang = 'lang' in kwargs and kwargs.pop('lang') or None
        super(IntakeIssueForm, self).__init__(*args, **kwargs)

        if lang == 'es':
            self.fields['safety_concerns'].choices = self.ES_CHOICES
            self.fields['reported_before'].choices = self.ES_CHOICES
            self.fields['how_many_people'].widget = forms.TextInput(attrs={'placeholder': 'ex: 4'})
            self.fields['time_of_day'].widget = forms.TextInput(attrs={'placeholder': 'ex: en la noche'})
            self.fields['how_long'].widget = forms.TextInput(attrs={'placeholder': u'ex: 3 días'.encode('utf-8')})
            self.fields['reported_before_details'].widget = forms.TextInput(attrs={'placeholder': 'ex: ayer, a Code Enforcement'})
            self.fields['problem_location'].widget = forms.TextInput(attrs={'placeholder': u'dirección o intersección'.encode('utf-8')})

        if lang == 'en' or lang is None:
            self.fields['safety_concerns'].choices = self.EN_CHOICES
            self.fields['reported_before'].choices = self.EN_CHOICES
            self.fields['how_many_people'].widget = forms.TextInput(attrs={'placeholder': 'ex: 4'})
            self.fields['time_of_day'].widget = forms.TextInput(attrs={'placeholder': 'ex: night'})
            self.fields['how_long'].widget = forms.TextInput(attrs={'placeholder': 'ex: 3 days'})
            self.fields['reported_before_details'].widget = forms.TextInput(attrs={'placeholder': 'ex: yesterday, to Code Enforcement'})
            self.fields['problem_location'].widget = forms.TextInput(attrs={'placeholder': 'address or intersection'})


class IntakeContactForm(forms.Form):
    error_css_class = 'form-error'

    EN_CONTACT_METHOD_CHOICES = [
        (CSSCall.NO_CONTACT_PREFERENCE, "I don't want to receive updates"),
        (CSSCall.EMAIL_CONTACT_PREFERENCE, 'Email'),
        (CSSCall.TEXT_CONTACT_PREFERENCE, 'Text Message')
    ]

    ES_CONTACT_METHOD_CHOICES = [
        (CSSCall.NO_CONTACT_PREFERENCE, "No quiero recibir actualizaciones"),
        (CSSCall.EMAIL_CONTACT_PREFERENCE, 'Email'),
        (CSSCall.TEXT_CONTACT_PREFERENCE, 'SMS')
    ]

    reporter_name = forms.CharField(required=False)
    reporter_phone = forms.CharField(required=False)
    reporter_address = forms.CharField(required=False)
    reporter_email = forms.EmailField(required=False)
    reporter_contact_method = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        lang = 'lang' in kwargs and kwargs.pop('lang') or None
        super(IntakeContactForm, self).__init__(*args, **kwargs)

        if lang == 'es':
            self.fields['reporter_contact_method'].choices = self.ES_CONTACT_METHOD_CHOICES

        if lang == 'en' or lang is None:
            self.fields['reporter_contact_method'].choices = self.EN_CONTACT_METHOD_CHOICES

    def clean(self, *args, **kwargs):
        data = super(IntakeContactForm, self).clean(*args, **kwargs)

        if not data.get('reporter_email') and data.get('reporter_contact_method') == 'email':
            raise forms.ValidationError('You chose to receive email updates but did not provide an email address.')

        if not data.get('reporter_phone') and data.get('reporter_contact_method') == 'text':
            raise forms.ValidationError('You chose to receive email updates but did not provide a phone number.')


class IntakeQuestionForm(forms.Form):
    question = forms.CharField()


class IntakeMessageForm(forms.Form):
    message = forms.CharField()
