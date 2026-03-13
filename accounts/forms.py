from django import forms
from django.contrib.auth.models import User
from .models import Profile
from services.models import Category, City

class RegisterForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"}))
    phone_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Create a secret password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}))
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, widget=forms.Select(attrs={"class": "form-select", "onchange": "toggleProviderFields()"}))
    
    # Provider specific fields
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="Select Category", widget=forms.Select(attrs={"class": "form-select"}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, empty_label="Select City", widget=forms.Select(attrs={"class": "form-select"}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Short Bio / Experience"}))
    profile_photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Choose a username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "name@example.com"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        role = cleaned_data.get("role")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        if role == 'provider':
            required_provider_fields = ['full_name', 'phone_number', 'category', 'city']
            for field in required_provider_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f"This field is required for Providers.")
        
        return cleaned_data