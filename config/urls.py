"""URLs for fincore-django project."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('wallets/', include('apps.wallets.urls')),
    path('transactions/', include('apps.transactions.urls')),
]