from gae import forms
from apps.user.models import LocalUser

class UserLoginForm(forms.ModelForm):
    '''Login form'''
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model  = LocalUser
        fields = ['nick', 'password']

class UserRegistrationForm(forms.ModelForm):
    '''Registration form'''
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model  = LocalUser
        fields = ['nick', 'password']