# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MyUserCreationForm(UserCreationForm):
    error_messages = {
        'duplicate_username': u"Użytkownik o takiej nazwie już istnieje.",
        'password_mismatch': u"Podane hasła różnią się.",
        'duplicate_email': u"Na podany e-mail został już zarejestrowany inny użytkownik",
    }

    username = forms.RegexField(label=u"Login", max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': u"To pole może zawierać tylko litery, cyfry lub "
                         "znaki @ . + - _"},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login', 'required': True,}),
        required=True)
    email = forms.EmailField(label=u"Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail', 'required': True,}),
        required=True)
    password1 = forms.CharField(label=u"Hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Hasło', 'required': True,}),
        required=True)
    password2 = forms.CharField(label=u"Potwierdź hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Potwierdź hasło', 'required': True,}),
        required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')            

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def as_bootstrap(self):
        return self._html_output(
            normal_row = '%(field)s%(help_text)s',
            error_row = '%s',
            row_ender = '\n',
            help_text_html = ' <span class="helptext">%s</span>',
            errors_on_separate_row = False)

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user