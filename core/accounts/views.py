from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages
from zoneinfo import available_timezones
from django.utils.timezone import activate
from .forms import SignUpForm, CustomLoginForm


@csrf_exempt
def set_timezone(request):
    if request.method == 'POST':
        tz = request.POST.get('timezone')
        if tz in available_timezones():
            request.session['user_timezone'] = tz
            activate(tz)  # Activate it immediately for the response
            return HttpResponse("Timezone set")
    return HttpResponse("Invalid timezone", status=400)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')
        else:
            # Display form errors (automatically handled in the template)
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect(reverse('dashboard')) 
    
    if request.method == 'POST':
        username = request.POST['login-username']
        password = request.POST['login-password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/app/dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    login_form = CustomLoginForm(prefix='login')
    signup_form = SignUpForm(prefix='signup')
    return render(request, "home.html", {
        "login_form": login_form,
        "signup_form": signup_form
    })