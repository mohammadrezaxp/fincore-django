# FinCore — Secure Django Digital Wallet & Ledger

FinCore is a robust, production-grade Django digital wallet web application featuring an append-only, double-entry financial ledger and secure wallet-to-wallet transfers. Designed as a demonstration and portfolio project.

## Project Overview
FinCore implements secure ledger-backed accounting. It ensures every transaction is fully balanced, immutable, and resistant to race conditions or silent divergence between account balances and ledger entries.

## Key Backend Features
- **Double-Entry Ledger:** Append-only ledger supporting LedgerAccount, LedgerTransaction, and LedgerEntry models.
- **Atomic Transfers:** Wallet updates and ledger postings execute within a single atomic database transaction.
- **Idempotency Enforcement:** Database-level uniqueness constraints on idempotency keys to prevent duplicate transaction processing.
- **Strict Validation:** Comprehensive validation preventing negative balances, self-transfers, currency mismatches, and unauthorized access.

## Technology Stack
- **Backend:** Python 3.14, Django 5.1
- **Database:** SQLite (default for development), PostgreSQL-ready
- **Frontend:** Server-rendered Django templates with modern responsive CSS

## Project Architecture
```
fincore-django/
├── apps/
│   ├── accounts/     # User auth & profile management
│   ├── core/         # Landing and core views
│   ├── transactions/ # Double-entry ledger, transfer service & views
│   └── wallets/      # Wallet models & dashboard views
├── config/           # Django settings, URLs, WSGI/ASGI
├── templates/        # HTML templates matching FinCore design specs
└── tests/            # Automated test suite
```

## Installation and Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/username/fincore-django.git
   cd fincore-django
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements/base.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Run development server:
   ```bash
   python manage.py runserver
   ```

## Database Migrations
To apply migrations and verify the database schema:
```bash
python manage.py makemigrations --check --dry-run
python manage.py migrate
```

## How to Run Tests
Execute the full automated test suite with verbosity:
```bash
python manage.py test -v 2
```

## Security Measures
- **CSRF Protection:** Enabled globally on all POST forms.
- **Authentication Required:** Protected endpoints enforce login.
- **Object-Level Authorization:** Users can only view their own wallets and transaction history.
- **Decimal Precision:** Strict usage of `Decimal` fields to prevent floating-point rounding errors in financial computations.

## Known Limitations
- **SQLite Concurrency:** SQLite does not support true row-level locking via `select_for_update()`. For high-throughput concurrent environments, PostgreSQL is strongly recommended.

## Screenshots
*(Placeholders for application dashboard, transfer form, and transaction history screenshots)*

## Disclaimer
FinCore is a simulation and portfolio project. It does not integrate with real banking systems, payment gateways, or live financial networks.
