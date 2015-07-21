from django.contrib import admin
from django import forms
# from django.db import models
from intake.models import Call
from intake.widgets import NameRecordingFieldWidget, AddressRecordingFieldWidget, DescriptionRecordingFieldWidget


class CallAdmin(admin.ModelAdmin):
    fields = ('call_sid', 'caller_name', 'name_recording_url', 'call_time', 'caller_number', 'caller_preferred_contact', 'problem_address', 'address_recording_url', 'problem_description', 'description_recording_url',)
    readonly_fields = ('call_sid', 'call_time', 'caller_number', 'caller_preferred_contact')
    list_display = ('call_sid', 'call_time', 'caller_name', 'caller_number', 'problem_address',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'name_recording_url':
             kwargs['widget'] = NameRecordingFieldWidget
        if db_field.name == 'address_recording_url':
             kwargs['widget'] = AddressRecordingFieldWidget
        if db_field.name == 'description_recording_url':
             kwargs['widget'] = DescriptionRecordingFieldWidget

        if db_field.name == 'problem_description':
            return forms.CharField(widget=forms.Textarea(attrs={'cols': 90, 'rows':12, 'class': 'docx'}))

        return super(CallAdmin, self).formfield_for_dbfield(db_field,**kwargs)

admin.site.register(Call, CallAdmin)
