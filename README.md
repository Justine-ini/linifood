# linifood

linifood is a Django food ordering marketplace where vendors can manage
restaurant profiles and menus, while customers can browse food items, add them
to a cart, and place orders.

## Features

- Custom user accounts for customers and vendors
- Vendor registration and restaurant profile management
- Menu categories and food item management
- Marketplace browsing and search
- Cart and checkout flow
- Order records with ordered food line items
- Customer and vendor dashboards
- Email template structure for account and order notifications
- Static frontend assets and reusable Django templates

## Tech Stack

- Python
- Django 5.0
- MySQL
- python-decouple for environment configuration
- Pillow for uploaded images
- HTML, CSS, JavaScript, and Bootstrap-style templates

## Project Structure

```text
linifood_main/  Django project settings, URLs, and static assets
accounts/       Custom users, authentication, and profiles
vendor/         Vendor registration and restaurant profile records
menu/           Food categories and food items
marketplace/    Listings, search, cart, and checkout views
customers/      Customer dashboard and order history
orders/         Payments, orders, and ordered food records
templates/      Shared and app-specific Django templates
static/         Frontend assets
```

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL server
- A virtual environment tool such as `venv`

### Local Setup

Clone the repository:

```bash
git clone https://github.com/Justine-ini/linifood.git
cd linifood
```

Create and activate a virtual environment:

```bash
python -m venv env
env\Scripts\activate
```

Install the project dependencies. This repository currently does not include a
`requirements.txt`, so install the core dependencies used by the project:

```bash
pip install django mysqlclient python-decouple pillow
```

Create a `.env` file from the sample:

```bash
copy .env-sample .env
```

Fill in the required values:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=linifood
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

Run migrations and start the development server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Notes

- Environment variables should stay in `.env`; do not commit secrets.
- Uploaded media, database files, local virtual environments, editor history,
  and generated cache files should stay out of git.
- The next improvements should be tests, a dependency lock/requirements file,
  screenshots, and deployment documentation.

## Status

This is a portfolio Django marketplace project. It is being cleaned up so the
repository presents the application clearly to visitors and collaborators.
