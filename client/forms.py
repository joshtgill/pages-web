from django import forms


class OrganizationForm(forms.Form):
    organization = forms.CharField(label='',
                                   widget=forms.TextInput(attrs={'placeholder': 'Explore an organization', 'autocomplete': 'off'}),
                                   max_length=100)
    # page = forms.IntegerField(widget = forms.HiddenInput(), required=False)


class PageForm(forms.Form):
    organization = forms.CharField(label='',
                                   widget=forms.TextInput(attrs={'placeholder': 'Explore an organization', 'autocomplete': 'off'}),
                                   max_length=100)
    page = forms.IntegerField()
