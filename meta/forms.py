from django import forms


class CreateAccountForm(forms.Form):

    firstName = forms.CharField(label='',
                                widget=forms.TextInput(attrs={'id': 'fullNameInput',
                                                              'placeholder': 'First name',
                                                              'autocomplete': 'off'}),
                                max_length=100)

    lastName = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'id': 'lastNameInput',
                                                             'placeholder': 'Last name',
                                                             'autocomplete': 'off'}),
                               max_length=100)

    email = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'id': 'emailInput',
                                                          'placeholder': 'Email',
                                                          'autocomplete': 'off'}),
                            max_length=100)

    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'id': 'passwordInput',
                                                                 'placeholder': 'Password'}))

    repeatPassword = forms.CharField(label='',
                                     widget=forms.PasswordInput(attrs={'id': 'repeatPasswordInput',
                                                                       'placeholder': 'Repeat password'}))


class LoginForm(forms.Form):

    email = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'id': 'emailInput',
                                                          'placeholder': 'Email',
                                                          'autocomplete': 'off'}),
                            max_length=100)

    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'id': 'passwordInput',
                                                                 'placeholder': 'Password'}))