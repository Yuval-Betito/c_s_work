from django import forms
from .models import User
import json
import re
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Load configuration from the JSON file
        with open('password_config.json', 'r') as f:
            config = json.load(f)

        # Check password length
        if len(password) < config['min_length']:
            raise ValidationError(f"Password must be at least {config['min_length']} characters long.")

        # Check for uppercase, lowercase, digits, and special characters
        if config['require_uppercase'] and not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if config['require_lowercase'] and not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if config['require_digit'] and not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.")
        if config['require_special'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        user.set_password(password)  # Use the overridden set_password method
        if commit:
            user.save()
        return user
