from django import forms

from django.contrib.auth.models import User
from django.forms.widgets import Select, CheckboxInput, ClearableFileInput

from workflow.models import CSSCase


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class StatusModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class PriorityModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CSSCaseDetailsForm(forms.ModelForm):

    # assignee = UserModelChoiceField(queryset=User.objects.all(), required=False)
    # assignee = forms.CharField(required=False)

    class Meta:
        model = CSSCase

        fields = (
            'case_no',
            'description',
            'resolution',
            'priority',
            # 'assignee'
        )

    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop('readonly')
        super(CSSCaseDetailsForm, self).__init__(*args, **kwargs)

        if readonly:
            for field in self.fields:
                if isinstance(self.fields[field].widget, Select):
                    self.fields[field].widget.attrs['disabled'] = True
                elif isinstance(self.fields[field].widget, CheckboxInput):
                    self.fields[field].widget.attrs['disabled'] = True
                elif isinstance(self.fields[field].widget, ClearableFileInput):
                    self.fields[field].widget.attrs['disabled'] = True
                else:
                    self.fields[field].widget.attrs['readonly'] = True
