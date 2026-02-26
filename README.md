# TAP Digital Business Card - Django Backend

A Django-based web application for TAP digital business cards with persistent checkout form data storage.

## Features

- Digital business card checkout form with data persistence
- **Dynamic pricing management from Django admin panel**
- File upload support for profile pictures and company logos
- Social media link management
- Django admin interface for order management
- Chapa payment gateway integration
- Responsive design with modern UI
- Shopping cart functionality with localStorage
- Automatic cleanup of failed payment attempts

## Technology Stack

- **Backend**: Django 6.0.2
- **Database**: SQLite (development)
- **Frontend**: HTML5, CSS3, JavaScript
- **Image Processing**: Pillow 12.1.0

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd NFC-website-design
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Chapa Payment Gateway

1. Sign up for a Chapa account at [https://dashboard.chapa.co](https://dashboard.chapa.co)
2. Get your API keys from Settings → API Keys
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Update `.env` with your Chapa credentials:
   ```
   CHAPA_SECRET_KEY=your-actual-secret-key
   CHAPA_PUBLIC_KEY=your-actual-public-key
   ```

Alternatively, update `src/settings.py` directly (not recommended for production):
```python
CHAPA_SECRET_KEY = 'your-chapa-secret-key'
CHAPA_PUBLIC_KEY = 'your-chapa-public-key'
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account for accessing the Django admin interface.

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### 9. Set Up Dynamic Pricing (Important!)

After running migrations, populate the initial pricing data:

```bash
python manage.py populate_pricing
```

This creates the 4 default pricing plans. You can then manage pricing from the Django admin panel.

For detailed instructions on managing pricing, see [PRICING_SETUP.md](PRICING_SETUP.md).

## Project Structure

```
NFC-website-design/
├── checkout/               # Main Django app
│   ├── models.py          # Database models (CheckoutSubmission, SocialMediaLink)
│   ├── views.py           # View logic for pages
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin interface configuration
│   └── urls.py            # App URL patterns
├── src/                   # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/             # HTML templates
│   ├── base.html          # Base template with common elements
│   ├── home.html          # Homepage
│   ├── store.html         # Store page
│   ├── contact.html       # Contact page
│   ├── card_detail.html   # Card detail page
│   └── checkout/          # Checkout templates
│       ├── checkout.html  # Checkout form
│       └── success.html   # Order success page
├── static/                # Static files (CSS, JS, images)
│   ├── styles.css         # Main stylesheet
│   ├── js/cart.js         # Shopping cart logic
│   └── images/            # Image assets
├── media/                 # User uploaded files
│   └── profiles/          # Profile pictures and logos
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Usage

### Accessing the Application

- **Homepage**: `http://127.0.0.1:8000/`
- **Store**: `http://127.0.0.1:8000/store/`
- **Checkout**: `http://127.0.0.1:8000/checkout/`
- **Contact**: `http://127.0.0.1:8000/contact/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

### Payment Flow

1. User fills out checkout form with personal information
2. System redirects to Chapa payment gateway
3. After payment, Chapa redirects back to verify endpoint
4. System verifies payment with Chapa API
5. If successful, user is redirected to success page
6. If failed, user can retry (old pending orders are automatically cleaned up)

### Failed Payment Retry

The system now allows users to retry payments if they fail:
- Only paid orders block email reuse
- Pending/failed orders older than 1 hour are automatically cleaned up
- Users can submit a new order with the same email after a failed payment

### Cleaning Up Old Orders

Run the management command to clean up old pending orders:

```bash
# Clean up orders older than 24 hours (default)
python manage.py cleanup_pending_orders

# Clean up orders older than 6 hours
python manage.py cleanup_pending_orders --hours 6
```

You can set up a cron job or scheduled task to run this periodically.

### Admin Interface

1. Navigate to `http://127.0.0.1:8000/admin/`
2. Log in with your superuser credentials
3. View and manage:
   - **Card Pricing**: Manage pricing plans, features, and badges
   - Checkout submissions
   - Social media links
   - User accounts

### Managing Orders

The admin interface provides:
- Search functionality by name, email, or order ID
- Filtering by subscription type and date
- Detailed view of each order including uploaded files
- Export capabilities

## Database Models

### CardPricing

Manages pricing plans displayed on the website:
- Plan information (name, subtitle, price, card range)
- Features list (multi-line text)
- Display options (badges, order, active status)
- Fully manageable from Django admin panel

### CheckoutSubmission

Stores customer order information:
- Personal information (name, title, email)
- Visual identity (profile picture, company logo)
- Subscription details (type, amount)
- Timestamps (created, updated)

### SocialMediaLink

Stores social media links associated with orders:
- Platform (LinkedIn, Twitter, Instagram, etc.)
- URL
- Foreign key relationship to CheckoutSubmission

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

After modifying models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Django Shell

```bash
python manage.py shell
```

## Configuration

### Settings

Key settings in `src/settings.py`:

- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain in production
- `DATABASES`: Configure production database
- `STATIC_ROOT`: Static files collection directory
- `MEDIA_ROOT`: User uploaded files directory

### Static Files

Static files are served from the `static/` directory during development. For production, run:

```bash
python manage.py collectstatic
```

### Media Files

User uploaded files (profile pictures, logos) are stored in the `media/` directory.

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Configure static file serving (nginx, whitenoise, etc.)
5. Set up media file storage (S3, local storage, etc.)
6. Use a production WSGI server (gunicorn, uwsgi)
7. Configure HTTPS/SSL
8. Set up environment variables for sensitive data

## Troubleshooting

### Static Files Not Loading

```bash
python manage.py collectstatic --clear
```

### Database Issues

```bash
python manage.py migrate --run-syncdb
```

### Port Already in Use

```bash
python manage.py runserver 8080
```

## Support

For issues or questions:
- Email: info@tap.et
- Phone: 0927-34-73-54 / 0936-51-51-36
- Website: https://tap.et

## License

Copyright © 2025 TAP - Digital Business Card. All rights reserved.
