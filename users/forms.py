from django import forms
from .models import User
import json
import re
from django.core.exceptions import ValidationError
from django.conf import settings  # לשימוש ב-BASE_DIR

def validate_password_with_config(password):
    """Validate password against the rules in password_config.json"""
    with open(settings.BASE_DIR / 'password_config.json', 'r') as f:
        config = json.load(f)

    # בדיקות על בסיס קובץ התצורה
    if len(password) < config['min_length']:
        raise ValidationError(f"Password must be at least {config['min_length']} characters long.")
    if config['require_uppercase'] and not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if config['require_lowercase'] and not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if config['require_digit'] and not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit.")
    if config['require_special'] and not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")

class PasswordChangeCustomForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # מקבל את המשתמש שעדכן את הסיסמה
        super().__init__(*args, **kwargs)

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        validate_password_with_config(new_password)  # בדיקת סיסמה חדשה

        # בדיקה מול היסטוריית הסיסמאות
        if self.user:
            if any(hmac.compare_digest(old.split('$')[1], new_password) for old in self.user.password_history[-3:]):
                raise ValidationError("New password cannot match any of the last 3 passwords.")

        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        if new_password and new_password != confirm_new_password:
            raise ValidationError("New passwords do not match.")
        return cleaned_data
