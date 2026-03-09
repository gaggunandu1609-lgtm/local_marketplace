from django.shortcuts import render, get_object_or_404
from .models import ServiceProvider

def home(request):
    providers = ServiceProvider.objects.all()[:6]
    return render(request, "home.html", {"services": providers})

def services_view(request):
    providers = ServiceProvider.objects.all()
    return render(request, "services.html", {"services": providers})

def service_detail(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    return render(request, "service_details.html", {"service": provider})