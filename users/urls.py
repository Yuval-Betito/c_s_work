from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),  # נתיב לפאנל הניהול של Django
    path('', include('users.urls')),  # חיבור ל-urls של האפליקציה users (הנתיב הראשי)

    # נתיבים לשינוי סיסמה
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),

    # נתיבים לשכחתי סיסמה ואיפוס סיסמה
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),

    # נתיב להתנתקות
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # התנתקות עם הפניה למסך כניסה
    
    # הוספת הנתיב הזה לכניסה
    path('login/', auth_views.LoginView.as_view(), name='login'),  # זה הנתיב הנכון ל-login
]
