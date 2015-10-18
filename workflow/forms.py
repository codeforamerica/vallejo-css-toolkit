from django import forms

from workflow.models import CSSCall, CSSCase, CaseStatus

from django.contrib.auth.models import User


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class StatusModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CSSCallForm(forms.ModelForm):

    class Meta:
        model = CSSCall

        fields = (
            'name',
            'address',
            'phone',
            'problem',
            'date',
            'resolution',
            'reported_datetime',
            'tags',
            'reporter_address_number',
            'reporter_street_name',
            'when_last_reported',
            'time_of_day_occurs',
            'num_people_involved',
            'safety_concerns',
            'reporter_alternate_contact'
        )


class CSSCaseDetailsForm(forms.ModelForm):

    assignee = UserModelChoiceField(queryset=User.objects.all())
    status = StatusModelChoiceField(queryset=CaseStatus.objects.all())

    class Meta:
        model = CSSCase

        fields = (
            'description',
            'resolution',
            'status',
            'address_number',
            'street_name'
        )


class CSSCaseOwnerForm(forms.ModelForm):

    class Meta:
        model = CSSCase

        fields = (
            'owner_name',
            'owner_address',
            'owner_phone',
            'owner_email'
        )
