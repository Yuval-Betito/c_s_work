import json
import re
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import User

# פונקציה לבדוק סיסמאות לפי הקובץ password_config.json
def validate_password_with_config(password, user=None):
    """Validate password against the rules in password_config.json"""
    
    # טוען את הגדרות הסיסמה מקובץ JSON
    with open(settings.BASE_DIR / 'password_config.json', 'r') as f:
        config = json.load(f)

    # בדיקות על בסיס קובץ התצורה
    if len(password) < config['min_password_length']:
        raise ValidationError(f"Password must be at least {config['min_password_length']} characters long.")
    if config['password_requirements']['uppercase'] and not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if config['password_requirements']['lowercase'] and not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if config['password_requirements']['digits'] and not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit.")
    if config['password_requirements']['special_characters'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")
    
    # בדיקה שהסיסמה לא כוללת מילים מתוך מילון
    if config.get('dictionary_check', False):
        common_words = ['password', '123456', 'qwerty', 'admin', 'letmein']  # דוגמה למילים מהותיות שמומלץ להימנע מהן
        if any(word in password.lower() for word in common_words):
            raise ValidationError("Password contains common words that are too easy to guess.")
    
    # אם יש היסטוריית סיסמאות, נוודא שהסיסמה החדשה אינה חוזרת על סיסמאות קודמות
    if user and user.password_history:
        password_history = user.password_history.split(",")  # ההיסטוריה מופרדת בפסיק
        if password in password_history:
            raise ValidationError("You cannot use one of your last 3 passwords.")
    
    return password


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

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        validate_password_with_config(new_password)  # בדיקת סיסמה חדשה
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        if new_password and new_password != confirm_new_password:
            raise ValidationError("New passwords do not match.")
        return cleaned_data

    def save(self, user, commit=True):
        new_password = self.cleaned_data.get('new_password')
        user.set_password(new_password)
        user.password_history = user.password_history + "," + new_password  # עדכון היסטוריית הסיסמאות
        if len(user.password_history.split(",")) > settings.PASSWORD_HISTORY:
            user.password_history = ",".join(user.password_history.split(",")[-settings.PASSWORD_HISTORY:])  # שמירה על 3 סיסמאות אחרונות
        if commit:
            user.save()
        return user


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
