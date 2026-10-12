from apps.wallets.models import Wallet
"""Transactions app models: Double-entry ledger."""
import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class LedgerAccount(models.Model):
    ACCOUNT_TYPES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('revenue', 'Revenue'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ledger_accounts',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.currency})"


class LedgerTransaction(models.Model):
    idempotency_key = models.UUIDField(unique=True, editable=False)
    reference = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='posted')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tx {self.idempotency_key} [{self.status}]"


class LedgerEntry(models.Model):
    ENTRY_TYPES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]
    transaction = models.ForeignKey(
        LedgerTransaction,
        on_delete=models.CASCADE,
        related_name='entries'
    )
    account = models.ForeignKey(
        LedgerAccount,
        on_delete=models.CASCADE,
        related_name='entries'
    )
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Entry amount must be positive.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name='ledger_entry_amount_gt_0'
            )
        ]

    def __str__(self):
        return f"{self.entry_type}: {self.amount} {self.currency} on {self.account.name}"

class TransferRecord(models.Model):
    idempotency_key = models.UUIDField(unique=True)
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='sent_transfers')
    recipient_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    ledger_transaction = models.ForeignKey(LedgerTransaction, on_delete=models.CASCADE)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
