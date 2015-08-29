from django import forms

from workflow.models import CSSCall

class CSSCallForm(forms.ModelForm):
    class Meta:
        model = CSSCall

        fields = (
            'id',
            'name',
            'address',
            'phone',
            'problem',
            'date',
            'resolution'
        )
