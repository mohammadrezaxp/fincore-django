from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
import uuid
from apps.transactions.models import LedgerAccount, LedgerTransaction, LedgerEntry
from apps.transactions.services import post_transaction

class LedgerTests(TestCase):
    def setUp(self):
        self.asset_acc = LedgerAccount.objects.create(name='Cash', account_type='asset')
        self.equity_acc = LedgerAccount.objects.create(name='Capital', account_type='equity')

    def test_balanced_transaction(self):
        idemp = uuid.uuid4()
        entries = [
            {'account': self.asset_acc, 'entry_type': 'debit', 'amount': Decimal('100.00')},
            {'account': self.equity_acc, 'entry_type': 'credit', 'amount': Decimal('100.00')}
        ]
        tx = post_transaction(idemp, entries)
        self.assertEqual(tx.entries.count(), 2)

    def test_unbalanced_transaction_rejected(self):
        idemp = uuid.uuid4()
        entries = [
            {'account': self.asset_acc, 'entry_type': 'debit', 'amount': Decimal('100.00')},
            {'account': self.equity_acc, 'entry_type': 'credit', 'amount': Decimal('50.00')}
        ]
        with self.assertRaises(ValidationError):
            post_transaction(idemp, entries)

    def test_idempotency(self):
        idemp = uuid.uuid4()
        entries = [
            {'account': self.asset_acc, 'entry_type': 'debit', 'amount': Decimal('100.00')},
            {'account': self.equity_acc, 'entry_type': 'credit', 'amount': Decimal('100.00')}
        ]
        tx1 = post_transaction(idemp, entries)
        tx2 = post_transaction(idemp, entries)
        self.assertEqual(tx1.id, tx2.id)
