from django import forms
from django.contrib.auth.forms import AuthenticationForm

class StyledLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 mt-1 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all',
            'placeholder': 'Enter your username',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-2 mt-1 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all',
            'placeholder': 'Enter your password',
        })
