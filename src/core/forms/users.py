from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from ..models import PersonalData


class CreateUserForm(UserCreationForm):
    """Create New User Form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.help_text = None

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserPersonalDataForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        exclude = ("user",)
