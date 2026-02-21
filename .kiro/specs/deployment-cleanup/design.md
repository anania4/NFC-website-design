# Design Document: Deployment Cleanup

## Overview

This design outlines the systematic approach to cleaning up the TAP Digital Business Card Django project for production deployment. The cleanup process will remove duplicate files, development artifacts, and configure the application for production use while maintaining all necessary functionality.

## Architecture

The cleanup process follows a phased approach:

1. **File Removal Phase**: Remove duplicate and unnecessary files
2. **Configuration Phase**: Update Django settings for production
3. **Dependencies Phase**: Add production-specific packages
4. **Documentation Phase**: Create deployment guides

### Directory Structure (After Cleanup)

```
NFC-website-design/
├── checkout/               # Django app (unchanged)
├── src/                   # Django project settings
│   └── settings.py        # Updated for production
├── templates/             # HTML templates (unchanged)
├── static/                # Static files (unchanged)
├── staticfiles/           # Collected static files
├── media/                 # User uploads (unchanged)
├── .env.example           # Environment variables template
├── manage.py              # Django management script
├── requirements.txt       # Updated with production packages
├── DEPLOYMENT.md          # New deployment guide
└── README.md              # Updated documentation
```

## Components and Interfaces

### 1. File Removal Component

**Purpose**: Systematically remove unnecessary files

**Files to Remove**:
- Root HTML files: `card-detail.html`, `checkout.html`, `contact.html`, `store.html`, `tap_new.html`, `mobile-test.html`
- Duplicate static files: `styles.css` (root), `images/` (root), `js/` (root)
- Development files: `test_chapa.py`, `checkoutmigrations__init__.py`
- Documentation files: `DEBUGGING_STEPS.md`, `CHAPA_INTEGRATION.md`, `PAYMENT_FLOW.md`
- Database: `db.sqlite3`

**Interface**: File system operations (delete)

### 2. Settings Configuration Component

**Purpose**: Update Django settings for production security and performance

**Changes Required**:
```python
# src/settings.py

import os
from decouple import config

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# Chapa Configuration
CHAPA_SECRET_KEY = config('CHAPA_SECRET_KEY')
CHAPA_PUBLIC_KEY = config('CHAPA_PUBLIC_KEY')

# Static Files (with WhiteNoise)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security Settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

**Interface**: Python configuration file

### 3. Environment Variables Component

**Purpose**: Externalize sensitive configuration

**.env.example Template**:
```
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Chapa Payment Gateway
CHAPA_SECRET_KEY=your-chapa-secret-key
CHAPA_PUBLIC_KEY=your-chapa-public-key

# Security (Production)
SECURE_SSL_REDIRECT=True

# Database (if using PostgreSQL in production)
DATABASE_URL=postgresql://user:password@localhost/dbname
```

**Interface**: Environment file

### 4. Dependencies Component

**Purpose**: Add production-specific packages

**Updated requirements.txt**:
```
asgiref==3.11.1
Django==6.0.2
pillow==12.1.0
sqlparse==0.5.5
tzdata==2025.3

# Production packages
gunicorn==21.2.0
whitenoise==6.6.0
python-decouple==3.8
```

**Interface**: Python package file

## Data Models

No changes to existing data models. The cleanup process does not affect:
- CheckoutSubmission model
- SocialMediaLink model
- Database schema

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: File Removal Completeness
*For any* file in the removal list, after cleanup execution, that file should not exist in the file system.
**Validates: Requirements 1.1, 1.4, 2.1, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1**

### Property 2: Template Preservation
*For any* template file in the templates/ directory, after cleanup execution, that file should still exist unchanged.
**Validates: Requirements 1.3**

### Property 3: Static Files Preservation
*For any* file in static/images/ or static/js/ directories, after cleanup execution, that file should still exist unchanged.
**Validates: Requirements 2.4**

### Property 4: Environment Variable Externalization
*For any* sensitive configuration value (SECRET_KEY, CHAPA keys), after configuration update, that value should be loaded from environment variables and not hardcoded in settings.py.
**Validates: Requirements 5.3, 5.4**

### Property 5: Production Security Settings
*For any* production deployment, DEBUG should be False and security middleware should be enabled.
**Validates: Requirements 5.1, 5.5**

### Property 6: Dependencies Completeness
*For any* production-required package (gunicorn, whitenoise, python-decouple), after requirements update, that package should be listed in requirements.txt.
**Validates: Requirements 6.1, 6.2, 6.3, 6.4**

## Error Handling

### File Removal Errors
- **Error**: File not found during removal
- **Handling**: Log warning and continue (file may already be removed)
- **Recovery**: No action needed

### Configuration Errors
- **Error**: Missing environment variable
- **Handling**: Raise clear error message indicating which variable is missing
- **Recovery**: User must set environment variable

### Static Files Collection Errors
- **Error**: Permission denied during collectstatic
- **Handling**: Display error with permission requirements
- **Recovery**: User must fix file permissions

## Testing Strategy

### Unit Tests
- Test environment variable loading with python-decouple
- Test settings configuration with different DEBUG values
- Test ALLOWED_HOSTS parsing from comma-separated string

### Manual Testing
- Verify all duplicate files are removed
- Verify templates still render correctly
- Verify static files are served correctly
- Verify environment variables are loaded
- Verify production settings are applied

### Deployment Testing
- Test collectstatic command
- Test gunicorn server startup
- Test WhiteNoise static file serving
- Test with DEBUG=False
- Test with production database

## Deployment Guide Structure

The DEPLOYMENT.md file will include:

1. **Pre-Deployment Checklist**
   - Environment variables configured
   - Database ready
   - Static files collected

2. **Environment Setup**
   - Creating .env file
   - Setting environment variables

3. **Database Migration**
   - Running migrations on production database
   - Creating superuser

4. **Static Files**
   - Collecting static files
   - Configuring web server

5. **Server Configuration**
   - Gunicorn setup
   - Nginx/Apache configuration (if applicable)
   - SSL/HTTPS setup

6. **Post-Deployment**
   - Health checks
   - Monitoring setup
   - Backup configuration
