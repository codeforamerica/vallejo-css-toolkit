from django.contrib import admin

from intake.models import Call

class CallAdmin(admin.ModelAdmin):
    pass

admin.site.register(Call, CallAdmin)
