from django import forms


class OrganizationForm(forms.Form):
    organization = forms.CharField(label='',
                                   widget=forms.TextInput(attrs={'placeholder': 'Explore an organization', 'autocomplete': 'off'}),
                                   max_length=100)


class PageForm(forms.Form):
    organization = forms.CharField(label='',
                                   widget=forms.TextInput(attrs={'placeholder': 'Explore an organization', 'autocomplete': 'off'}),
                                   max_length=100)
    page = forms.IntegerField()


class RequestMembershipForm(forms.Form):
    organizationIdToRequestMembership = forms.IntegerField()


class EventAttendanceForm(forms.Form):
    eventId = forms.IntegerField()
    status = forms.BooleanField(required=False)
