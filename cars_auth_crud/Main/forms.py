from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core import validators
import re
from Main.models import *


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'owner': forms.HiddenInput(),  # Hide the field in the form
        }


class RegisterForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'password1']  # Only include the necessary fields

        # If you have a specific field to hide (like 'usa'), make sure it's in the model
        widgets = {
            'usable_password': forms.HiddenInput(),  # Example of hiding the username, adjust as needed
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user  # Return the user instance, not the form data
