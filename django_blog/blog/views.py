# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Login view using Django built-in
def login_view(request):
    from django.contrib.auth.forms import AuthenticationForm
    from django.contrib import messages

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        # allow user to update email
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
    return render(request, 'blog/profile.html', {'user': request.user})
