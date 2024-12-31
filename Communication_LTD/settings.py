from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-gl=b&u71jf7ix(s^b^+y8^!eiubw&i43$r+l%)yhw#!fju)(p@"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",  # האפליקציה users
    "axes",  # הוספת אפליקציה להגבלת ניסיונות Login
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "axes.middleware.AxesMiddleware",  # הוספת Middleware להגבלת ניסיונות Login
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Communication_LTD.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],  # תיקיית templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Communication_LTD.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},  # אורך סיסמה מינימלי
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "he"

TIME_ZONE = "Asia/Jerusalem"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

# הוספת לוגיקה לנתיב LOGOUT
LOGOUT_REDIRECT_URL = 'login'  # מפנה לדף הלוגין לאחר התנתקות

# הוספת URL ברירת מחדל למקרה שאין למשתמש הרשאות
LOGIN_URL = '/login/'

# נתיב לדף הבית לאחר התחברות
LOGIN_REDIRECT_URL = '/'  # דף הבית לאחר התחברות

# הוספת מייל לשליחת טוקנים
DEFAULT_FROM_EMAIL = 'no-reply@communication_ltd.com'  # כתובת המייל לשליחת טוקנים

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# הגבלת ניסיונות Login
AXES_FAILURE_LIMIT = 3  # מספר ניסיונות כושלים לפני חסימה
AXES_LOCK_OUT_AT_FAILURE = True  # חסימה לאחר כישלון
AXES_RESET_COOL_OFF_ON_FAILURE_DURING_LOCKOUT = True  # איפוס חסימה אחרי זמן מסוים


# מניעת שימוש בסיסמאות מילון
PASSWORD_DICTIONARY_PATH = BASE_DIR / "common_passwords.txt"
AUTH_PASSWORD_VALIDATORS.append({
    "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    "OPTIONS": {
        "dictionary_path": str(PASSWORD_DICTIONARY_PATH)
    },
})
