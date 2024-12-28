import hmac
import hashlib
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .forms import RegisterForm, CustomerForm
from .models import User


def verify_password(stored_password, entered_password):
    """Verify password by comparing entered password with the stored hash"""
    try:
        salt, stored_hash = stored_password.split('$')
        entered_hash = hmac.new(salt.encode(), entered_password.encode(), hashlib.sha256).hexdigest()
        return stored_hash == entered_hash
    except ValueError:
        return False


def user_login(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect('add_customer')  # Redirect to add_customer
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})

    return render(request, 'users/login.html')


def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


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
        return response


def password_change_done(request):
    """Display password change success message"""
    return render(request, 'users/password_change_done.html')


def create_customer(request):
    """Handle creating a new customer"""
    customer = None

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        phone_number = request.POST.get('phone_number', '').strip()

        if form.is_valid():
            if phone_number.startswith("05") and phone_number.isdigit() and len(phone_number) == 10:
                customer = form.save(commit=False)
                customer.phone_number = phone_number
                customer.save()
                form = CustomerForm()  # Reset the form after saving
            else:
                form.add_error('phone_number', "Please enter a valid Israeli phone number.")
        else:
            form.add_error(None, "Invalid data submitted. Please check the form fields.")

    else:
        form = CustomerForm()

    return render(request, 'users/create_customer.html', {'form': form, 'customer': customer})
