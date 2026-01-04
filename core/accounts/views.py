"""
Views for user authentication and account management.

Handles user signup, login, logout, and timezone preferences.
"""

from zoneinfo import available_timezones

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, reverse
from django.utils.timezone import activate
from django.views.decorators.http import require_POST

from .forms import CustomLoginForm, SignUpForm


@login_required
@require_POST
def set_timezone(request):
    """Set the user's timezone preference in their session."""
    tz = request.POST.get('timezone')
    if tz and tz in available_timezones():
        request.session['user_timezone'] = tz
        activate(tz)
        return JsonResponse({'success': True, 'timezone': tz})
    return JsonResponse({'success': False, 'error': 'Invalid timezone'}, status=400)

def signup_view(request):
    """Handle user registration with form validation."""
    if request.method == 'POST':
        print("POST data:", request.POST)
    
        # Add this to see which template Django finds
        from django.template.loader import get_template
        template = get_template('accounts/signup.html')
        print("Template path:", template.origin.name)
        
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')
        else:
            # Loop through each field's errors
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        # Non-field errors (like password mismatch)
                        messages.error(request, error)
                    else:
                        # Field-specific errors
                        messages.error(request, f"{field.title()}: {error}")
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Handle user authentication and login."""
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')

def logout_view(request):
    """Log out the current user and redirect to home."""
    logout(request)
    return redirect('home')


def home_view(request):
    login_form = CustomLoginForm()
    signup_form = SignUpForm()
    
    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return render(request, 'home.html', context)