from django import forms


class SelectOrganizationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.choices = [(organization.id, organization.name) for organization in kwargs.pop('organizations')]
        super(SelectOrganizationForm, self).__init__(*args, **kwargs)

        self.fields['ids'] = forms.ChoiceField(label='', choices=self.choices, required=True)


class BuilderForm(forms.Form):
    typee = forms.CharField()
    idd = forms.IntegerField(required=False)


class PageDeleteForm(forms.Form):
    pageIdToDelete = forms.IntegerField()


class OrganizationEditForm(forms.Form):
    name = forms.CharField()
    private = forms.BooleanField(required=False)


class LeaveOrganizationForm(forms.Form):
    leaveOrganization = forms.BooleanField()
