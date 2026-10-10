"""Wallets app views."""
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wallet

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        return render(request, 'wallets/dashboard.html', {'wallet': wallet})


class WalletView(LoginRequiredMixin, View):
    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        return render(request, 'wallets/wallet.html', {'wallet': wallet})


class TransferView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'wallets/transfer.html')
