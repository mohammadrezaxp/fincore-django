"""Transactions app URLs."""
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.TransactionListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.TransactionDetailView.as_view(), name='detail'),
]