from gae import forms
from models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model   = Message
        exclude = ['author']