from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from django.contrib.auth import authenticate, login as django_login, logout
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User  # Import the custom User model

# הגבלת מספר ניסיונות ההתחברות
MAX_LOGIN_ATTEMPTS = settings.MAX_LOGIN_ATTEMPTS  # הגדרה מקובץ settings.py

# פונקציה שתעבוד כאשר יש הצלחה בהתחברות
@receiver(user_logged_in)
def reset_login_attempts(sender, request, user, **kwargs):
    """Reset login attempts when the user successfully logs in."""
    user.failed_login_attempts = 0
    user.last_failed_login = None
    user.save()

# פונקציה שתעבוד כאשר יש כישלון בהתחברות
@receiver(user_login_failed)
def track_failed_login_attempt(sender, request, credentials, **kwargs):
    """Track failed login attempts and block the user after exceeding the maximum attempts."""
    username = credentials.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return  # If the user does not exist, do nothing

    # Update the number of failed login attempts
    if user.failed_login_attempts is None:
        user.failed_login_attempts = 1
    else:
        user.failed_login_attempts += 1

    # If the number of failed attempts exceeds the limit, block the user
    if user.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
        user.last_failed_login = timezone.now()  # Store the time of the last failed attempt
        user.save()
        raise ValidationError("You have reached the maximum number of login attempts. Please try again later.")
    else:
        user.save()

def user_login(request):
    """Handle user login with limited attempts."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        except ValidationError as e:
            messages.error(request, str(e))  # Show error if the user has exceeded max login attempts
    return render(request, 'users/login.html')


# פונקציה להודעה על שינוי סיסמה
def password_change_done(request):
    """Display password change success message."""
    return render(request, 'users/password_change_done.html')


# פונקציה להתנתקות מהמערכת
def logout_view(request):
    """Logout the user and redirect to login page."""
    logout(request)
    return redirect('login')  # הפנייה לדף הלוגין לאחר התנתקות

