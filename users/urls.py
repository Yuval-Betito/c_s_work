from django.urls import path
from .views import register, user_login, home, create_customer  # ייבוא הפונקציות מ-views

# URLs עבור האפליקציה users
urlpatterns = [
    path('register/', register, name='register'),  # נתיב לרישום משתמשים חדשים
    path('login/', user_login, name='login'),      # נתיב לכניסה למערכת
    path('', home, name='home'),                   # דף הבית (נתיב ריק)
    path('customer/add/', create_customer, name='add_customer'),  # הוספת לקוח חדש
]
