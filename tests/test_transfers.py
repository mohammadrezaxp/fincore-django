from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
import uuid
from django.core.exceptions import ValidationError
from apps.transactions.services import transfer_funds
from apps.transactions.models import TransferRecord
from apps.wallets.models import Wallet

User = get_user_model()

class TransferServiceTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='password123')
        self.user2 = User.objects.create_user(username='bob', password='password123')
        Wallet.objects.create(user=self.user1, balance=Decimal('500.00'), currency='USD')
        Wallet.objects.create(user=self.user2, balance=Decimal('0.00'), currency='USD')

    def test_successful_transfer(self):
        idemp = uuid.uuid4()
        rec = transfer_funds(self.user1, 'bob', Decimal('150.00'), idempotency_key=idemp, note='Gift')
        self.assertIsInstance(rec, TransferRecord)
        self.user1.wallet.refresh_from_db()
        self.user2.wallet.refresh_from_db()
        self.assertEqual(self.user1.wallet.balance, Decimal('350.00'))
        self.assertEqual(self.user2.wallet.balance, Decimal('150.00'))

    def test_insufficient_funds(self):
        with self.assertRaises(ValidationError):
            transfer_funds(self.user1, 'bob', Decimal('600.00'))

    def test_self_transfer_rejected(self):
        with self.assertRaises(ValidationError):
            transfer_funds(self.user1, 'alice', Decimal('50.00'))

    def test_idempotent_transfer(self):
        idemp = uuid.uuid4()
        rec1 = transfer_funds(self.user1, 'bob', Decimal('100.00'), idempotency_key=idemp)
        rec2 = transfer_funds(self.user1, 'bob', Decimal('100.00'), idempotency_key=idemp)
        self.assertEqual(rec1.pk, rec2.pk)
        self.user1.wallet.refresh_from_db()
        self.assertEqual(self.user1.wallet.balance, Decimal('400.00'))
