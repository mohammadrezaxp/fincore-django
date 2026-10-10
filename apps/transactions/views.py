"""Transactions app views."""
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


class TransactionListView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'transactions/list.html')


class TransactionDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'transactions/detail.html')
