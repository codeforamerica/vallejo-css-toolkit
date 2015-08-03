from django import forms

from django.contrib.auth.models import User

from intake.models import Call

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()

class CallForm(forms.ModelForm):

    assignee = UserModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        fields = (
            'id',
            'problem_description',
            'caller_name',
            'caller_number',
            'problem_address',
            'name_recording_url',
            'property_owner',
            'property_owner_phone',
            'assignee',
            'status',
            'call_time',
            'name_recording_url',
            'description_recording_url',
            'address_recording_url'
        )

        model = Call

    def __init__(self, *args, **kwargs):
        super(CallForm, self).__init__(*args, **kwargs)
        self.fields['call_time'].widget.attrs['readonly'] = True
        self.fields['name_recording_url'].widget.attrs['readonly'] = True
        self.fields['description_recording_url'].widget.attrs['readonly'] = True
        self.fields['address_recording_url'].widget.attrs['readonly'] = True
