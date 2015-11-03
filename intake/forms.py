from django import forms


class IntakeIssueForm(forms.Form):

    CHOICES = [
        ('yes', ' Yes'),
        ('no', ' No'),
        ('unsure', "I'm not sure")
    ]

    problem_location = forms.CharField()
    how_many_people = forms.CharField()
    time_of_day = forms.CharField()
    how_long = forms.CharField()
    description = forms.CharField()
    uploaded_photo = forms.FileField()
    safety_concerns = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    reported_before = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    reported_before_details = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(IntakeIssueForm, self).__init__(*args, **kwargs)

        self.fields['how_many_people'].widget = forms.TextInput(attrs={'placeholder': 'ex: 4'})
        self.fields['time_of_day'].widget = forms.TextInput(attrs={'placeholder': 'ex: night'})
        self.fields['how_long'].widget = forms.TextInput(attrs={'placeholder': 'ex: 3 days'})
        self.fields['reported_before_details'].widget = forms.TextInput(attrs={'placeholder': 'ex: yesterday, to Code Enforcement'})
        self.fields['problem_location'].widget = forms.TextInput(attrs={'placeholder': 'Address or cross street'})
