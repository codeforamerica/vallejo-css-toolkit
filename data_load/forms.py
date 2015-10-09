from django import forms

file_type_choices = [
    ('CSS calls', 'CSS calls'),
    ('CSS cases', 'CSS cases'),
    ('RMS cases', 'RMS cases'),
]

class UploadFileForm(forms.Form):
    file  = forms.FileField()
    file_type = forms.ChoiceField(choices=file_type_choices)
