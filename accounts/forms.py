# -*- coding: utf-8 -*-
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, AuthenticationForm, \
    UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from accounts.models import Person
from main.functions import add_form_control_class


class PasswordChangeFormEdited(PasswordChangeForm):
    meta = {'title': _('Change password'), 'button': _('Save'), 'action': '',
            'form_class': 'col-lg-8 col-lg-offset-2', 'header_class': 'header-form-profile'}

    def __init__(self, *args, **kwargs):
        super(PasswordChangeFormEdited, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': self.fields['old_password'].label})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control input_reset_password', 'placeholder': self.fields['new_password1'].label})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control input_reset_password', 'placeholder': self.fields['new_password2'].label})


class PasswordResetFormEdited(PasswordResetForm):
    meta = {'title': _('Reset password'), 'button': _('Reset'), 'action': '',
            'form_class': 'col-lg-8 col-lg-offset-2', 'header_class': 'header-form-profile'}

    def __init__(self, *args, **kwargs):
        super(PasswordResetFormEdited, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control input_reset_password', 'placeholder': self.fields['email'].label})


class SetPasswordFormEdited(SetPasswordForm):
    meta = {'title': _('Reset password'), 'button': _('Save'), 'action': '',
            'form_class': 'col-lg-8 col-lg-offset-2', 'header_class': 'header-form-profile'}

    def __init__(self, *args, **kwargs):
        super(SetPasswordFormEdited, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control form-first input_reset_password',
                                                          'placeholder': self.fields['new_password1'].label})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control form-last input_reset_password', 'placeholder': self.fields['new_password2'].label})


class AuthenticationFormEdited(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationFormEdited, self).__init__(*args, **kwargs)
        #self.fields['username'].label = _('email')
        add_form_control_class(self.fields)

class SingUpForm(UserCreationForm):
    class Meta:

        model = Person
        fields = ('first_name','last_name','email')

    def __init__(self, *args, **kwargs):
        super(SingUpForm, self).__init__(*args, **kwargs)
        # self.fields['username'].label = _('email')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        add_form_control_class(self.fields)

class UserForm(UserCreationForm):
    class Meta:
        model = Person
        fields = ('username', 'email', 'first_name','last_name','password1', 'password2', 'dni', 'sex')
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _('usuario')
        self.fields['email'].label = _('Correo')

        self.fields['first_name'].label = "Nombres"
        self.fields['last_name'].label = "Apellidos"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirme Contraseña"
        self.fields['sex'].label = "Sexo"

        add_form_control_class(self.fields)
