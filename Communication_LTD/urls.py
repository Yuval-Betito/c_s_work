from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # נתיב לפאנל הניהול של Django
    path('', include('communication.urls')),  # כולל את הנתיבים של אפליקציית ה-communication
    path('users/', include('users.urls')),  # כולל את הנתיבים של אפליקציית ה-users
]
