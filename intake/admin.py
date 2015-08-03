from django.contrib import admin
from intake.models import Call, CallAuditItem
from intake.widgets import NameRecordingFieldWidget, AddressRecordingFieldWidget, DescriptionRecordingFieldWidget

from intake.forms import CallForm

class CallAdmin(admin.ModelAdmin):
    fields = ('call_sid', 'caller_name', 'name_recording_url', 'call_time', 'caller_number', 'caller_preferred_contact', 'problem_address', 'address_recording_url', 'problem_description', 'description_recording_url',)
    readonly_fields = ('call_sid', 'call_time', 'caller_number')#, 'caller_preferred_contact')
    list_display = ('call_sid', 'call_time', 'caller_name', 'caller_number', 'problem_address',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'name_recording_url':
             kwargs['widget'] = NameRecordingFieldWidget
        if db_field.name == 'address_recording_url':
             kwargs['widget'] = AddressRecordingFieldWidget
        if db_field.name == 'description_recording_url':
             kwargs['widget'] = DescriptionRecordingFieldWidget

        return super(CallAdmin, self).formfield_for_dbfield(db_field,**kwargs)

class CallAuditItemAdmin(admin.ModelAdmin):

    fields = ('call', 'user', 'timestamp', 'changed_field', 'old_value', 'new_value')
    readonly_fields = ('call', 'user', 'timestamp', 'changed_field', 'old_value', 'new_value')
    list_display = ('call', 'user', 'timestamp')


admin.site.register(Call, CallAdmin)
admin.site.register(CallAuditItem, CallAuditItemAdmin)
