from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm
)
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
    )
    name = forms.CharField(
        max_length=30,
        required=True,
        label='Имя',
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        label='Почта',
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'name',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'
            field.widget.attrs['placeholder'] = field.label


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input'
            field.widget.attrs['placeholder'] = field.label


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'placeholder': 'Старый пароль', 'class': 'input'}
        )
        self.fields['new_password1'].widget.attrs.update(
            {'placeholder': 'Новый пароль', 'class': 'input'}
        )
        self.fields['new_password2'].widget.attrs.update(
            {'placeholder': 'Подтвердите новый пароль', 'class': 'input'}
        )