from django import forms
from .models import User, Customer
import json
import re
from django.core.exceptions import ValidationError
from django.conf import settings  # לשימוש ב-BASE_DIR

# פונקציה לבדוק סיסמאות לפי הקובץ password_config.json
def validate_password_with_config(password, user=None):
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
    if config['require_digit'] and not re.search(r'\\d', password):
        raise ValidationError("Password must contain at least one digit.")
    if config['require_special'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")

    # מניעת שימוש בסיסמאות מילון
    if config['dictionary_check']:
        common_passwords = ["123456", "password", "qwerty"]  # דוגמה לרשימת מילים נפוצות
        if password in common_passwords:
            raise ValidationError("Password cannot be a common password.")

    # מניעת שימוש בסיסמאות מהיסטוריה (אם משתמש מוגדר)
    if user and config['history_check']:
        hashed_passwords = [entry.split('$')[1] for entry in user.password_history]
        if any(re.search(hashed, password) for hashed in hashed_passwords):
            raise ValidationError("Password cannot match the last used passwords.")

# טופס רישום משתמש
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password_with_config(password)  # בדיקת הסיסמה
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        user.set_password(password)  # הצפנת הסיסמה
        if commit:
            user.save()
        return user

# טופס שינוי סיסמה
class PasswordChangeCustomForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        validate_password_with_config(new_password, user=self.user)  # בדיקת סיסמה חדשה
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        if new_password and new_password != confirm_new_password:
            raise ValidationError("New passwords do not match.")
        return cleaned_data

# טופס ליצירת לקוח חדש
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'customer_id', 'phone_number', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ערך ברירת מחדל לשדה phone_number
        self.fields['phone_number'].widget.attrs.update({'value': '05'})

    def save(self, commit=True):
        customer = super().save(commit=False)
        if commit:
            customer.save()
        return customer
