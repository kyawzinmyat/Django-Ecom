from .models import UserBase
from django import forms

class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label = 'Username',
        min_length = 6,
        help_text = 'Required'
    )
    email = forms.EmailField(max_length=150, help_text= 'Required', error_messages={'required' : 'Required Email'})
    password = forms.CharField(label = 'Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Repeat Password', widget = forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email')