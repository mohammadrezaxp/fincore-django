"""Wallets app URLs."""
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('transfer/', views.TransferView.as_view(), name='transfer'),
]