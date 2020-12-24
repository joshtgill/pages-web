from django import forms


class PageForm(forms.Form):
    name = forms.CharField()
