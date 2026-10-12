from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import TransferForm
from django.contrib import messages
from apps.transactions.models import LedgerEntry

class TransferView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'wallets/transfer.html', {'form': TransferForm()})

    def post(self, request):
        form = TransferForm(request.POST)
        if form.is_valid():
            # Implement transfer logic
            pass
        return render(request, 'wallets/transfer.html', {'form': form})

class TransactionListView(LoginRequiredMixin, View):
    def get(self, request):
        # Fetch entries for the user
        return render(request, 'wallets/transactions.html') # Corrected template
