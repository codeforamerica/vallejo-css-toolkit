from django.contrib import admin

from intake.models import Call

class CallAdmin(admin.ModelAdmin):
    # fields = ('call_sid', 'caller_name', 'name_recording_url', 'caller_number', 'caller_preferred_contact', 'problem_address', 'address_recording_url', 'problem_description', 'description_recording_url',)
    # readonly_fields = ('name_recording_url', 'call_time',)
    list_display = ('call_sid', 'call_time', 'caller_name', 'caller_number', 'problem_address',)

admin.site.register(Call, CallAdmin)
