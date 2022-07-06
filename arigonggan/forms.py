from django import forms

class UserForm(forms.Form):
    userId = forms.CharField(label="userId")