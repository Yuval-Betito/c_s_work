from django.urls import path
from .views import register, user_login, home  # Use the renamed user_login view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
]
