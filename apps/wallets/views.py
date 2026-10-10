"""Wallets app views (placeholders)."""
from django.views import View
from django.shortcuts import render


class DashboardView(View):
    def get(self, request):
        return render(request, 'wallets/dashboard.html')


class WalletView(View):
    def get(self, request):
        return render(request, 'wallets/wallet.html')


class TransferView(View):
    def get(self, request):
        return render(request, 'wallets/transfer.html')