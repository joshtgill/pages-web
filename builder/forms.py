from django import forms


class SelectOrganizationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.choices = [(organization.id, organization.name) for organization in kwargs.pop('organizations')]
        super(SelectOrganizationForm, self).__init__(*args, **kwargs)

        self.fields['ids'] = forms.ChoiceField(label='', choices=self.choices, required=True)


class RegisterOrganizationForm(forms.Form):
    name = forms.CharField()
    headquarters = forms.CharField()
    description = forms.CharField()


class BuildForm(forms.Form):
    type = forms.CharField()
    idd = forms.IntegerField(required=False)


class DeletePageForm(forms.Form):
    pageIdToDelete = forms.IntegerField()


class EditOrganizationForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    isPrivate = forms.BooleanField(required=False)
    colorId = forms.IntegerField()


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
