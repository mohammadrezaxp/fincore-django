from django.test import TestCase
from django.contrib.auth.models import User
from apps.wallets.models import Wallet
from decimal import Decimal

class WalletTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!')

    def test_wallet_created_on_access(self):
        self.client.login(username='testuser', password='Password123!')
        self.client.get('/wallets/dashboard/')
        self.assertTrue(Wallet.objects.filter(user=self.user).exists())
        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(wallet.balance, Decimal('0.00'))

    def test_only_one_wallet_per_user(self):
        self.client.login(username='testuser', password='Password123!')
        self.client.get('/wallets/dashboard/')
        self.client.get('/wallets/dashboard/')
        self.assertEqual(Wallet.objects.filter(user=self.user).count(), 1)

    def test_negative_balance_constraint(self):
        wallet = Wallet.objects.create(user=self.user, balance=Decimal('0.00'))
        wallet.balance = Decimal('-10.00')
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            wallet.save()
