from django import forms


class OrganizationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.choices = [(organization.id, organization.name) for organization in kwargs.pop('organizations')]
        super(OrganizationForm, self).__init__(*args, **kwargs)

        self.fields['names'] = forms.ChoiceField(label='', choices=self.choices, required=True)


class BuilderForm(forms.Form):
    typee = forms.CharField()
    idd = forms.IntegerField(required=False)


class PageDeleteForm(forms.Form):
    pageIdToDelete = forms.IntegerField()
