from django.utils.safestring import mark_safe

from django import forms

class NameRecordingFieldWidget(forms.TextInput):
     def render(self, name, value, attrs=None):
        html = super(NameRecordingFieldWidget, self).render(name, value, attrs)
        if value:
            html =  """<audio controls><source src="%s.mp3" type="audio/mpeg"></audio><br/>""" % value + html.replace(' ', ' hidden ', 1)
        return mark_safe(html)

class AddressRecordingFieldWidget(forms.TextInput):
     def render(self, name, value, attrs=None):
        html = super(AddressRecordingFieldWidget, self).render(name, value, attrs)
        if value:
            html =  """<audio controls><source src="%s.mp3" type="audio/mpeg"></audio><br/>""" % value + html.replace(' ', ' hidden ', 1)
        return mark_safe(html)

class DescriptionRecordingFieldWidget(forms.TextInput):
     def render(self, name, value, attrs=None):
        html = super(DescriptionRecordingFieldWidget, self).render(name, value, attrs)
        if value:
            html =  """<audio controls><source src="%s.mp3" type="audio/mpeg"></audio><br/>""" % value + html.replace(' ', ' hidden ', 1)
        return mark_safe(html)
