from django import forms


class SelectOrganizationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.choices = [(organization.id, organization.name) for organization in kwargs.pop('organizations')]
        super(SelectOrganizationForm, self).__init__(*args, **kwargs)

        self.fields['ids'] = forms.ChoiceField(label='', choices=self.choices, required=True)


class RequestNewOrganizationForm(forms.Form):
    name = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': 'Organization name', 'autocomplete': 'off'}),
                           max_length=100)


class BuildForm(forms.Form):
    typee = forms.CharField()
    idd = forms.IntegerField(required=False)


class DeletePageForm(forms.Form):
    pageIdToDelete = forms.IntegerField()


class EditOrganizationForm(forms.Form):
    name = forms.CharField()
    isPrivate = forms.BooleanField(required=False)


class DeleteOrganizationForm(forms.Form):
    deleteOrganization = forms.BooleanField()


class ApproveMembershipForm(forms.Form):
    membershipIdToApprove = forms.IntegerField()


class DenyMembershipForm(forms.Form):
    membershipIdToDeny = forms.IntegerField()


class RevokeMembershipForm(forms.Form):
    membershipIdToRevoke = forms.IntegerField()


class LeaveOrganizationForm(forms.Form):
    leaveOrganization = forms.BooleanField()
