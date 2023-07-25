from django import forms
from ussd.models import UssdSession


class UsddForm(forms.ModelForm):
    class Meta:
        model = UssdSession
        fields = "__all__"