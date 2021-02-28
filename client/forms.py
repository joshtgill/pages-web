from django import forms


class OrganizationSearchForm(forms.Form):
    organizationName = forms.CharField(label='',
                                       widget=forms.TextInput(attrs={'placeholder': 'Explore an organization', 'autocomplete': 'off'}),
                                       max_length=100)
