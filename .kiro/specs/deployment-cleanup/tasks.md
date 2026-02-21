# Implementation Plan: Deployment Cleanup

## Overview

This plan outlines the step-by-step process to clean up the TAP Digital Business Card project for production deployment. Tasks are organized to ensure safe removal of unnecessary files while preserving all required functionality.

## Tasks

- [ ] 1. Backup current project state
  - Create a backup of the entire project before making changes
  - Verify backup is complete and accessible
  - _Requirements: All (safety measure)_

- [x] 2. Remove duplicate HTML files from root directory
  - Delete card-detail.html from root
  - Delete checkout.html from root
  - Delete contact.html from root
  - Delete store.html from root
  - Delete tap_new.html from root
  - Delete mobile-test.html from root
  - Verify templates/ directory still contains all necessary templates
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 3. Remove duplicate static files from root directory
  - Delete styles.css from root directory
  - Delete images/ directory from root
  - Delete js/ directory from root
  - Verify static/styles.css exists
  - Verify static/images/ directory exists
  - Verify static/js/ directory exists
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 4. Remove development and debug files
  - Delete test_chapa.py
  - Delete checkoutmigrations__init__.py
  - Delete DEBUGGING_STEPS.md
  - Delete CHAPA_INTEGRATION.md
  - Delete PAYMENT_FLOW.md
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 5. Remove development database
  - Delete db.sqlite3
  - Document that production will need fresh database setup
  - _Requirements: 4.1, 4.2, 4.3_

- [x] 6. Update requirements.txt with production packages
  - Add gunicorn==21.2.0
  - Add whitenoise==6.6.0
  - Add python-decouple==3.8
  - Keep all existing dependencies
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [x] 7. Create .env.example file
  - Create .env.example with all required environment variables
  - Include SECRET_KEY placeholder
  - Include DEBUG setting
  - Include ALLOWED_HOSTS placeholder
  - Include CHAPA_SECRET_KEY placeholder
  - Include CHAPA_PUBLIC_KEY placeholder
  - Include SECURE_SSL_REDIRECT setting
  - Add comments explaining each variable
  - _Requirements: 5.3, 5.4_

- [ ] 8. Update src/settings.py for production
  - [ ] 8.1 Add python-decouple imports
    - Import config from decouple
    - Import os module
    - _Requirements: 5.3, 5.4_

  - [x] 8.2 Update SECRET_KEY to use environment variable
    - Replace hardcoded SECRET_KEY with config('SECRET_KEY')
    - _Requirements: 5.3_

  - [x] 8.3 Update DEBUG to use environment variable
    - Replace DEBUG = True with config('DEBUG', default=False, cast=bool)
    - _Requirements: 5.1_

  - [x] 8.4 Update ALLOWED_HOSTS to use environment variable
    - Replace hardcoded ALLOWED_HOSTS with config parsing
    - Support comma-separated list of hosts
    - _Requirements: 5.2_

  - [x] 8.5 Update Chapa keys to use environment variables
    - Replace CHAPA_SECRET_KEY with config('CHAPA_SECRET_KEY')
    - Replace CHAPA_PUBLIC_KEY with config('CHAPA_PUBLIC_KEY')
    - _Requirements: 5.4_

  - [ ] 8.6 Add WhiteNoise middleware
    - Add 'whitenoise.middleware.WhiteNoiseMiddleware' to MIDDLEWARE
    - Place it after SecurityMiddleware
    - _Requirements: 5.5_

  - [ ] 8.7 Configure WhiteNoise static files storage
    - Add STATICFILES_STORAGE setting for WhiteNoise
    - _Requirements: 5.5_

  - [ ] 8.8 Add production security settings
    - Add SECURE_SSL_REDIRECT setting
    - Add SESSION_COOKIE_SECURE = True
    - Add CSRF_COOKIE_SECURE = True
    - Add SECURE_BROWSER_XSS_FILTER = True
    - Add SECURE_CONTENT_TYPE_NOSNIFF = True
    - _Requirements: 5.5_

- [ ] 9. Create DEPLOYMENT.md documentation
  - [ ] 9.1 Write Pre-Deployment Checklist section
    - List all prerequisites
    - Include environment variable setup
    - Include database preparation
    - _Requirements: 7.1_

  - [ ] 9.2 Write Environment Setup section
    - Document .env file creation
    - Document each environment variable
    - Provide example values
    - _Requirements: 7.2_

  - [ ] 9.3 Write Database Migration section
    - Document migration commands
    - Document superuser creation
    - _Requirements: 7.4_

  - [ ] 9.4 Write Static Files Collection section
    - Document collectstatic command
    - Document static file serving options
    - _Requirements: 7.3_

  - [ ] 9.5 Write Server Configuration section
    - Document gunicorn setup
    - Document web server configuration
    - Document SSL/HTTPS setup
    - _Requirements: 7.5_

- [ ] 10. Update README.md
  - Update deployment section to reference DEPLOYMENT.md
  - Update configuration section for environment variables
  - Remove references to deleted files
  - Update installation instructions
  - _Requirements: 7.1_

- [x] 11. Checkpoint - Verify cleanup is complete
  - Ensure all duplicate files are removed
  - Ensure all templates still exist
  - Ensure all static files still exist
  - Ensure settings.py is properly configured
  - Ensure requirements.txt includes production packages
  - Ensure documentation is complete
  - Ask the user if questions arise

## Notes

- All tasks should be executed in order
- Backup is created first as a safety measure
- File removal tasks are grouped by category
- Configuration tasks are broken down by specific setting
- Documentation tasks are comprehensive
- Final checkpoint ensures nothing was missed
