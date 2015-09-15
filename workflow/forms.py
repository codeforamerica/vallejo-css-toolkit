from django import forms

from workflow.models import CSSCall

from django.contrib.auth.models import User

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class CSSCallForm(forms.ModelForm):

    assignee = MyModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = CSSCall

        fields = (
            'id',
            'name',
            'address',
            'phone',
            'problem',
            'date',
            'resolution',
            'assignee'
        )
