from django import forms
from djangevu.forms import AjaxFormMixin
from django.contrib import messages


class NameForm(AjaxFormMixin, forms.Form):

    name = forms.CharField(
        max_length=254,
        min_length=5,
    )
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def save(self):
        print('Saved form!')
        messages.add_message(self.request, messages.INFO, 'Hello world! Form saved!')
