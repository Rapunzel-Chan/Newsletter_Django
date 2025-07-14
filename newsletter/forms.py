from django import forms
from newsletter.models import Mailing, Client, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['first_sending', 'message', 'clients']
        widgets = {
            'first_sending': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'message': forms.Select(attrs={'class': 'form-select'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['theme', 'content']
        widgets = {
            'theme': forms.TextInput(attrs={'placeholder': 'Введите тему сообщения'}),
            'content': forms.Textarea(attrs={'placeholder': 'Введите текст сообщения', 'rows': 5}),
        }

