urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('users.urls')),  # Connects the user app URLs to the root
    
    # Password change paths
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    
    # Password reset paths
    path('forgot_password/', views.forgot_password, name='forgot_password'),  # Ensure the view is implemented in views.py
    path('reset_password/', views.reset_password, name='reset_password'),  # Ensure the view is implemented in views.py
    
    # Logout path
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Login path
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
