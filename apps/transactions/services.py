"""Ledger service layer for atomic double-entry posting."""
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import LedgerTransaction, LedgerEntry, LedgerAccount


def post_transaction(idempotency_key, entries_data, reference=''):
    """
    Posts a balanced double-entry transaction atomically.
    entries_data format: [{'account': account_obj, 'entry_type': 'debit'/'credit', 'amount': Decimal, 'currency': 'USD'}, ...]
    """
    if not entries_data or len(entries_data) < 2:
        raise ValidationError("A transaction must have at least two entries.")

    with transaction.atomic():
        # Check idempotency
        if LedgerTransaction.objects.filter(idempotency_key=idempotency_key).exists():
            return LedgerTransaction.objects.get(idempotency_key=idempotency_key)

        # Validate sums per currency
        currency_sums = {}
        for ed in entries_data:
            curr = ed.get('currency', 'USD')
            amt = ed['amount']
            etype = ed['entry_type']
            if amt <= 0:
                raise ValidationError("Amounts must be strictly positive.")
            
            if curr not in currency_sums:
                currency_sums[curr] = Decimal('0.00')
            
            if etype == 'debit':
                currency_sums[curr] += amt
            elif etype == 'credit':
                currency_sums[curr] -= amt
            else:
                raise ValidationError(f"Invalid entry type: {etype}")

        for curr, net in currency_sums.items():
            if net != Decimal('0.00'):
                raise ValidationError(f"Unbalanced transaction for currency {curr}: net is {net}")

        # Create transaction
        tx = LedgerTransaction.objects.create(
            idempotency_key=idempotency_key,
            reference=reference
        )

        for ed in entries_data:
            LedgerEntry.objects.create(
                transaction=tx,
                account=ed['account'],
                entry_type=ed['entry_type'],
                amount=ed['amount'],
                currency=ed.get('currency', 'USD')
            )

        return tx
