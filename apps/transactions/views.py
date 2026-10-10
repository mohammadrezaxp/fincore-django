"""Transactions app views (placeholders)."""
from django.views import View
from django.shortcuts import render


class TransactionListView(View):
    def get(self, request):
        return render(request, 'transactions/list.html')


class TransactionDetailView(View):
    def get(self, request, pk):
        return render(request, 'transactions/detail.html')