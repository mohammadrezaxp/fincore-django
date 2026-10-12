"""Ledger service layer for atomic double-entry posting and wallet transfers."""
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import LedgerTransaction, LedgerEntry, LedgerAccount, TransferRecord
from apps.wallets.models import Wallet
import uuid

def post_transaction(idempotency_key, entries_data, reference=''):
    if not entries_data or len(entries_data) < 2:
        raise ValidationError("A transaction must have at least two entries.")

    with transaction.atomic():
        if LedgerTransaction.objects.filter(idempotency_key=idempotency_key).exists():
            return LedgerTransaction.objects.get(idempotency_key=idempotency_key)

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

        for curr, net in currency_sums.items():
            if net != Decimal('0.00'):
                raise ValidationError(f"Unbalanced transaction for currency {curr}")

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

def transfer_funds(sender, recipient_username, amount, idempotency_key=None, note=''):
    if sender.username == recipient_username:
        raise ValidationError("Cannot transfer to self.")
    if amount <= 0:
        raise ValidationError("Transfer amount must be positive.")
    if not idempotency_key:
        idempotency_key = uuid.uuid4()

    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        recipient = User.objects.get(username=recipient_username)
    except User.DoesNotExist:
        raise ValidationError("Recipient not found.")

    sender_wallet = sender.wallet
    recipient_wallet = recipient.wallet

    if sender_wallet.currency != recipient_wallet.currency:
        raise ValidationError("Currency mismatch.")

    with transaction.atomic():
        # Check existing transfer by idempotency key
        existing = TransferRecord.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing

        # Lock wallets in deterministic order by ID
        pk1, pk2 = sorted([sender_wallet.pk, recipient_wallet.pk])
        Wallet.objects.select_for_update().filter(pk=pk1)
        Wallet.objects.select_for_update().filter(pk=pk2)

        sender_wallet.refresh_from_db()
        recipient_wallet.refresh_from_db()

        if sender_wallet.balance < amount:
            raise ValidationError("Insufficient funds.")

        sender_wallet.balance -= amount
        sender_wallet.save()

        recipient_wallet.balance += amount
        recipient_wallet.save()

        # Get or create ledger accounts for wallets
        # Assuming asset/liability accounts or custom ledger accounts per wallet
        # For simplicity, create/get ledger accounts linked to users
        s_acc, _ = LedgerAccount.objects.get_or_create(user=sender, defaults={'name': f"{sender.username} Wallet", 'account_type': 'asset', 'currency': sender_wallet.currency})
        r_acc, _ = LedgerAccount.objects.get_or_create(user=recipient, defaults={'name': f"{recipient.username} Wallet", 'account_type': 'asset', 'currency': recipient_wallet.currency})

        entries = [
            {'account': s_acc, 'entry_type': 'credit', 'amount': amount, 'currency': sender_wallet.currency},
            {'account': r_acc, 'entry_type': 'debit', 'amount': amount, 'currency': recipient_wallet.currency}
        ]
        tx = post_transaction(idempotency_key, entries, reference=note or f"Transfer from {sender.username} to {recipient.username}")

        transfer_rec = TransferRecord.objects.create(
            idempotency_key=idempotency_key,
            sender_wallet=sender_wallet,
            recipient_wallet=recipient_wallet,
            amount=amount,
            currency=sender_wallet.currency,
            ledger_transaction=tx,
            note=note
        )
        return transfer_rec
