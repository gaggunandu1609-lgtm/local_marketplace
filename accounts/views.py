from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from .models import Profile

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
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
            
            full_name = form.cleaned_data.get("full_name", "")
            if full_name:
                name_parts = full_name.split(' ', 1)
                user.first_name = name_parts[0]
                if len(name_parts) > 1:
                    user.last_name = name_parts[1]
                user.save()

            # Profile is usually created by a signal if configured, 
            # but we'll manually ensure it here to be safe and set the role
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.phone = form.cleaned_data.get("phone_number", "")
            profile.save()

            if role == 'provider':
                # Ensure ServiceProvider object exists for providers
                from services.models import ServiceProvider
                provider, _ = ServiceProvider.objects.get_or_create(user=user, defaults={'business_name': full_name or user.username})
                provider.phone_number = form.cleaned_data.get("phone_number", "")
                provider.description = form.cleaned_data.get("bio", "")
                provider.category = form.cleaned_data.get("category")
                
                # Assign City if selected
                city_obj = form.cleaned_data.get("city")
                if city_obj:
                    provider.city_ref = city_obj
                    provider.area = city_obj.name # Optional: default area to city name
                    provider.latitude = 0.0
                    provider.longitude = 0.0
                
                # Check for profile_photo
                photo = form.cleaned_data.get('profile_photo')
                if photo:
                    provider.profile_photo = photo
                    
                provider.save()

            messages.success(request, f"Account created for {role} {username}! Please log in to continue.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.role == 'provider':
            return redirect('provider_dashboard')
        return redirect('/')
        
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            
            # Post-login redirect logic
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
                
            if hasattr(user, 'profile') and user.profile.role == 'provider':
                return redirect('provider_dashboard')
            return redirect('/')
        else:
            messages.error(request, 'Invalid email/username or password.')
            
    return render(request, 'login.html')