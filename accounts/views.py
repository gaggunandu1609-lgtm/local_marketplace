from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from .models import Profile

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]

            if User.objects.filter(username=username).exists():
                messages.error(request, f"The username '{username}' is already taken. Please choose another.")
                return render(request, "register.html", {"form": form})
            
            if User.objects.filter(email=email).exists():
                messages.error(request, f"The email '{email}' is already registered. Try logging in instead.")
                return render(request, "register.html", {"form": form})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Profile is usually created by a signal if configured, 
            # but we'll manually ensure it here to be safe and set the role
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()

            if role == 'provider':
                # Ensure ServiceProvider object exists for providers
                from services.models import ServiceProvider
                ServiceProvider.objects.get_or_create(user=user, defaults={'business_name': user.username})

            messages.success(request, f"Account created for {role} {username}! Please log in to continue.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})