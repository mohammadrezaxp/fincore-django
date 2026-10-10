"""Accounts app views (placeholders)."""
from django.views import View
from django.shortcuts import render


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')


class ProfileView(View):
    def get(self, request):
        return render(request, 'accounts/profile.html')