"""Wallets app models."""
import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.db.models import CheckConstraint, Q


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(balance__gte=0),
                name='wallet_balance_gte_0'
            )
        ]

    def __str__(self):
        return f"Wallet {self.public_id} ({self.user.username})"
