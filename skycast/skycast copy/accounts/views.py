from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_POST

# ✅ Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')  # 🔁 Redirect to login after registration
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# ✅ Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # 🔁 Redirect to home after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


# ✅ Logout view
@require_POST
def logout_view(request):
    logout(request)
    return redirect('register')  # 🔁 Redirect to register after logout
