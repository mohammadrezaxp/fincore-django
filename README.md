# FinCore Django - Digital Wallet Portfolio

A professional Django REST Framework digital wallet portfolio application.

## Project Structure

- `manage.py` - Django command-line utility
- `apps/` - Django applications (core, accounts, wallets, transactions)
- `config/` - Project configuration
- `templates/` - Base HTML templates
- `static/` - CSS, JS, images assets
- `media/` - User uploaded files
- `requirements/` - Python dependencies

## Quick Start

1. Install dependencies: `pip install -r requirements/dev.txt`
2. Migrate database: `python manage.py migrate`
3. Run server: `python manage.py runserver`
4. Visit: http://127.0.0.1:8000

## Apps

- `core` - Home page and base views
- `accounts` - User authentication (login/register/profile)
- `wallets` - Wallet dashboard and transactions
- `transactions` - Transaction ledger and detail views

## Development

- `python manage.py check` - System check
- `python manage.py migrate` - Run migrations
- `python manage.py test` - Run tests