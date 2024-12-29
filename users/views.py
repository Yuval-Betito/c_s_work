from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages  # For displaying messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, CustomerForm
from .models import User
import hashlib
import random


def user_login(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'users/login.html')


def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "There was an error in your registration. Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def home(request):
    """Render the home page"""
    return render(request, 'users/home.html')


class CustomPasswordChangeView(PasswordChangeView):
    """Custom view for handling password change"""
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        """Update the session after password change"""
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Your password was changed successfully.")
        return response


@login_required
def password_change_done(request):
    """Display password change success message"""
    return render(request, 'users/password_change_done.html')


@login_required
def create_customer(request):
    """Handle creating a new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f"Customer {customer.firstname} {customer.lastname} added successfully!")
            return redirect('home')
        else:
            messages.error(request, "Error in creating customer. Please check the form fields.")
    else:
        form = CustomerForm()

    return render(request, 'users/create_customer.html', {'form': form})


def forgot_password(request):
    """Handle forgot password functionality"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate reset token
            random_value = f"{random.randint(1000, 9999)}{user.username}"
            reset_token = hashlib.sha1(random_value.encode()).hexdigest()
            user.reset_token = reset_token
            user.save()
            messages.success(request, "Reset token sent to your email.")
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
    return render(request, 'users/forgot_password.html')


def reset_password(request):
    """Handle reset password functionality"""
    if request.method == 'POST':
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        try:
            user = User.objects.get(reset_token=token)
            user.set_password(new_password)
            user.reset_token = None  # Clear the reset token
            user.save()
            messages.success(request, "Password reset successfully.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Invalid reset token.")
    return render(request, 'users/reset_password.html')
