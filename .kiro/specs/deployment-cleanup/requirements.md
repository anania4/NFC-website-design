# Requirements Document: Deployment Cleanup

## Introduction

This specification outlines the cleanup process for the TAP Digital Business Card Django project to prepare it for production deployment by removing unnecessary files, duplicates, and development artifacts.

## Glossary

- **System**: The TAP Django web application
- **Deployment**: The process of making the application ready for production hosting
- **Duplicate_Files**: Files that exist in multiple locations with identical or similar content
- **Development_Artifacts**: Files used only during development (test files, debug files, etc.)

## Requirements

### Requirement 1: Remove Duplicate HTML Files

**User Story:** As a developer, I want to remove duplicate HTML files from the root directory, so that the project structure is clean and maintainable.

#### Acceptance Criteria

1. THE System SHALL remove standalone HTML files from the root directory that duplicate template files
2. WHEN HTML files exist in both root and templates directory, THE System SHALL keep only the templates directory version
3. THE System SHALL preserve all template files in the templates/ directory
4. THE System SHALL remove card-detail.html, checkout.html, contact.html, store.html, tap_new.html, and mobile-test.html from root

### Requirement 2: Remove Duplicate Static Files

**User Story:** As a developer, I want to consolidate static files, so that there is a single source of truth for CSS and JavaScript.

#### Acceptance Criteria

1. THE System SHALL remove duplicate styles.css from root directory
2. THE System SHALL keep styles.css in static/ directory only
3. THE System SHALL remove duplicate images/ and js/ directories from root
4. THE System SHALL preserve static/images/ and static/js/ directories

### Requirement 3: Remove Development and Debug Files

**User Story:** As a developer, I want to remove development-only files, so that the production deployment is clean and secure.

#### Acceptance Criteria

1. THE System SHALL remove test_chapa.py from root directory
2. THE System SHALL remove checkoutmigrations__init__.py from root directory
3. THE System SHALL remove DEBUGGING_STEPS.md documentation file
4. THE System SHALL remove CHAPA_INTEGRATION.md documentation file
5. THE System SHALL remove PAYMENT_FLOW.md documentation file

### Requirement 4: Clean Development Database

**User Story:** As a developer, I want to remove the development database, so that production starts with a fresh database.

#### Acceptance Criteria

1. THE System SHALL remove db.sqlite3 from root directory
2. WHEN deploying to production, THE System SHALL use a new database
3. THE System SHALL preserve database migrations in checkout/migrations/

### Requirement 5: Update Settings for Production

**User Story:** As a developer, I want to configure Django settings for production, so that the application is secure and performant.

#### Acceptance Criteria

1. THE System SHALL set DEBUG = False in settings.py
2. THE System SHALL configure ALLOWED_HOSTS for production domain
3. THE System SHALL move SECRET_KEY to environment variables
4. THE System SHALL move CHAPA_SECRET_KEY and CHAPA_PUBLIC_KEY to environment variables
5. THE System SHALL configure proper static file serving for production

### Requirement 6: Create Production Requirements File

**User Story:** As a developer, I want a production requirements file, so that deployment includes necessary production packages.

#### Acceptance Criteria

1. THE System SHALL add gunicorn to requirements.txt for production WSGI server
2. THE System SHALL add whitenoise to requirements.txt for static file serving
3. THE System SHALL add python-decouple to requirements.txt for environment variable management
4. THE System SHALL keep all existing dependencies in requirements.txt

### Requirement 7: Create Deployment Documentation

**User Story:** As a developer, I want deployment documentation, so that the application can be deployed consistently.

#### Acceptance Criteria

1. THE System SHALL create a DEPLOYMENT.md file with production deployment instructions
2. THE System SHALL document environment variable configuration
3. THE System SHALL document static file collection process
4. THE System SHALL document database migration process
5. THE System SHALL document production server setup
