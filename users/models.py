from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from django.contrib.auth import authenticate, login as django_login
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect


# הגבלת מספר ניסיונות ההתחברות
MAX_LOGIN_ATTEMPTS = settings.MAX_LOGIN_ATTEMPTS  # הגדרה מקובץ settings.py

# פונקציה שתעבוד כאשר יש הצלחה בהתחברות
@receiver(user_logged_in)
def reset_login_attempts(sender, request, user, **kwargs):
    # אפס את מספר הניסיונות אם המשתמש התחבר בהצלחה
    user.failed_login_attempts = 0
    user.last_failed_login = None
    user.save()

# פונקציה שתעבוד כאשר יש כישלון בהתחברות
@receiver(user_login_failed)
def track_failed_login_attempt(sender, request, credentials, **kwargs):
    username = credentials.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return  # אם המשתמש לא נמצא, אין מה לעשות

    # עדכון מספר הניסיונות
    if user.failed_login_attempts is None:
        user.failed_login_attempts = 1
    else:
        user.failed_login_attempts += 1

    # אם מספר הניסיונות עבר את המגבלה
    if user.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
        user.last_failed_login = timezone.now()  # שמור את הזמן האחרון שנעשו ניסיונות כושלים
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
            messages.error(request, str(e))  # הצגת שגיאה אם עברו את המגבלה
    return render(request, 'users/login.html')
