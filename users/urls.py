from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),  # נתיב למסך התחברות
    path('register/', views.register, name='register'),  # נתיב לרישום משתמש
    path('forgot_password/', views.forgot_password, name='forgot_password'),  # שכחתי סיסמה
    path('reset_password/', views.reset_password, name='reset_password'),  # איפוס סיסמה
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),  # שינוי סיסמה
    path('password_change_done/', views.password_change_done, name='password_change_done'),  # הודעה על שינוי סיסמה
    path('add_customer/', views.create_customer, name='add_customer'),  # יצירת לקוח חדש
    path('logout/', views.logout_view, name='logout'),  # התנתקות
]
