from django.urls import path
from .views import register, user_login, home, create_customer  # ייבוא הפונקציות מ-views

urlpatterns = [
    path('register/', register, name='register'),  # נתיב להרשמה
    path('login/', user_login, name='login'),  # נתיב לכניסה למערכת
    path('home/', home, name='home'),  # דף הבית
    path('customer/add/', create_customer, name='add_customer'),  # הוספת לקוח חדש
]
