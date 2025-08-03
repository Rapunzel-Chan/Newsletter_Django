from django import forms
from newsletter.models import Mailing, Client, Message


# class MailingForm(forms.ModelForm):
#     class Meta:
#         model = Mailing
#         fields = ["message", "clients"]
#         widgets = {
#             # "first_sending": forms.DateTimeInput(attrs={"type": "datetime-local"}),
#             "clients": forms.SelectMultiple(attrs={"class": "form-select"}),
#             "message": forms.Select(attrs={"class": "form-select"}),
#         }
class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["message", "clients"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["clients"].queryset = Client.objects.filter(owner=user)
            self.fields["message"].queryset = Message.objects.filter(owner=user)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["theme", "content"]
        widgets = {
            "theme": forms.TextInput(attrs={"placeholder": "Введите тему сообщения"}),
            "content": forms.Textarea(attrs={"placeholder": "Введите текст сообщения", "rows": 5}),
        }


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_classes} form-control".strip()
