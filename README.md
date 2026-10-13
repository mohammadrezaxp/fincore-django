# FinCore — Secure Django Digital Wallet & Ledger

FinCore is a backend portfolio and demonstration project built with Django, featuring an append-only, double-entry financial ledger and secure wallet-to-wallet transfers.

## Project Overview
FinCore demonstrates reliable financial accounting fundamentals within a simulated digital wallet environment. It is intended strictly for portfolio display and developer demonstration purposes, not for live banking or production financial operations.

## Key Backend Features
- **Double-Entry Ledger:** Append-only ledger structure comprising `LedgerAccount`, `LedgerTransaction`, and `LedgerEntry` models.
- **Atomic Transfers:** Wallet balance updates and ledger postings are executed within an atomic database transaction.
- **Idempotency Enforcement:** Database-level uniqueness constraints on transaction idempotency keys.
- **Strict Validation:** Guards against negative balances, self-transfers, and currency mismatches.

## Technology Stack
- **Backend:** Python 3.14, Django 6.1
- **Database:** SQLite (default development database)
- **Frontend:** Server-rendered Django templates with responsive CSS

## Project Architecture
```
fincore-django/
├── apps/
│   ├── accounts/     # User authentication & registration
│   ├── core/         # Core application views and home
│   ├── transactions/ # Double-entry ledger models, services & views
│   └── wallets/      # Wallet models & dashboard views
├── config/           # Django settings, URLs, WSGI/ASGI
├── templates/        # HTML templates matching the FinCore design
└── tests/            # Automated test suite
```

## Installation and Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/mohammadrezaxp/fincore-django.git
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
Verify migration consistency:
```bash
python manage.py makemigrations --check --dry-run
python manage.py migrate
```

## How to Run Tests
Run the automated test suite:
```bash
python manage.py test -v 2
```

## Security Measures
- **CSRF Protection:** Enabled across all form endpoints.
- **Authentication:** Login required for all wallet and transfer views.
- **Object Authorization:** Users can only access their own wallets and transfer histories.
- **Decimal Precision:** Uses `Decimal` for all monetary amounts to avoid float rounding errors.

## Known Limitations
- **SQLite Concurrency:** SQLite does not support true row-level locking via `select_for_update()`. For high-concurrency environments, PostgreSQL or MySQL with proper row locking is required.

## Screenshots
*(Insert application screenshots here)*

## Disclaimer
FinCore is a demonstration project and does not connect to real banking systems, payment gateways, or live financial networks.
