from django.contrib import admin

from intake.models import Call

class CallAdmin(admin.ModelAdmin):
    fields = ('call_sid', 'caller_name', 'name_recording_url', 'caller_number', 'caller_preferred_contact', 'problem_address', 'address_recording_url', 'problem_description', 'description_recording_url',)


admin.site.register(Call, CallAdmin)
