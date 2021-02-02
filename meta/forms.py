from django import forms


class CreateAccountForm(forms.Form):

    firstName = forms.CharField(label='',
                                widget=forms.TextInput(attrs={'placeholder': 'First name', 'autocomplete': 'off'}),
                                max_length=100)

    lastName = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Last name', 'autocomplete': 'off'}),
                               max_length=100)

    email = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off'}),
                            max_length=100)

    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    repeatPassword = forms.CharField(label='',
                                     widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))


class LoginForm(forms.Form):

    email = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off'}),
                            max_length=100)

    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class CreatorUpgradeForm(forms.Form):

    organization = forms.CharField(label='',
                                   widget=forms.TextInput(attrs={'placeholder': 'Organization', 'autocomplete': 'off'}),
                                   max_length=100)


class ChangeEmailForm(forms.Form):

    newEmail = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'placeholder': 'New email', 'autocomplete': 'off'}),
                               max_length=100)

    newEmailConfirm = forms.CharField(label='',
                                      widget=forms.TextInput(attrs={'placeholder': 'Confirm new email', 'autocomplete': 'off'}),
                                      max_length=100)


class ConfirmationForm(forms.Form):

    action = forms.CharField()
