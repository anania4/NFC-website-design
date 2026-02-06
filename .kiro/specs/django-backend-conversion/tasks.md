# Implementation Plan: Django Backend Conversion

## Overview

Convert the existing static HTML TAP digital business card website to a Django-based web application with persistent checkout form data storage while maintaining the existing frontend design and user experience.

## Tasks

- [x] 1. Create Django app and configure project structure
  - Create 'checkout' Django app for handling form submissions
  - Add checkout app to INSTALLED_APPS in settings
  - Configure static files and media handling in settings
  - Create templates directory structure
  - _Requirements: 1.1, 1.3, 5.1_

- [x] 2. Create database models and migrations
  - [x] 2.1 Implement CheckoutSubmission model
    - Create model with personal information fields (first_name, last_name, title, email)
    - Add visual identity fields (profile_picture, company_logo)
    - Include subscription type and amount fields
    - Add timestamps for creation and updates
    - _Requirements: 3.1, 3.3, 3.4_

  - [ ]* 2.2 Write property test for CheckoutSubmission model
    - **Property 1: Checkout Form Data Persistence**
    - **Validates: Requirements 3.1**

  - [x] 2.3 Implement SocialMediaLink model
    - Create model with platform choices and URL field
    - Link to CheckoutSubmission with foreign key relationship
    - Add unique constraint for submission-platform combination
    - _Requirements: 3.1_

  - [ ]* 2.4 Write property test for SocialMediaLink model
    - **Property 2: Social Media Link Processing**
    - **Validates: Requirements 3.1**

  - [x] 2.5 Create and run database migrations
    - Generate Django migrations for all models
    - Apply migrations to create database schema
    - _Requirements: 3.5_

- [x] 3. Create Django forms for checkout processing
  - [x] 3.1 Create CheckoutForm class
    - Create Django form with all required fields from checkout.html
    - Add form validation for personal information and file uploads
    - Include social media link processing fields
    - _Requirements: 2.1, 2.5_

  - [ ] 3.2 Write property test for form validation

    - **Property 6: Subscription Type and Amount Consistency**
    - **Validates: Requirements 2.1**

- [x] 4. Convert HTML templates to Django templates
  - [x] 4.1 Convert checkout.html to Django template
    - Convert static HTML to Django template with form integration
    - Add CSRF protection and Django form rendering
    - Preserve all existing CSS styling and JavaScript functionality
    - _Requirements: 1.3, 5.2, 5.4_

  - [x] 4.2 Convert tap_new.html to Django template
    - Convert to Django template with template inheritance
    - Update static file references to use Django static files
    - Preserve all existing animations and functionality
    - _Requirements: 1.4, 5.1, 5.2_

  - [x] 4.3 Convert store.html to Django template
    - Convert to Django template maintaining cart functionality
    - Update navigation links to use Django URL patterns
    - _Requirements: 1.4, 5.5_

  - [x] 4.4 Create base template and configure static files
    - Create base.html template with common elements
    - Set up template inheritance structure
    - Configure STATIC_URL and STATICFILES_DIRS in settings
    - _Requirements: 5.1, 5.3_

- [x] 5. Implement views and URL routing
  - [x] 5.1 Create CheckoutView
    - Implement view to display checkout form (GET request)
    - Handle form submission and validation (POST request)
    - Save valid form data to CheckoutSubmission model
    - Display success/error messages appropriately
    - _Requirements: 2.1, 2.2, 2.4_

  - [ ]* 5.2 Write property test for checkout processing
    - **Property 1: Checkout Form Data Persistence**
    - **Validates: Requirements 2.2**

  - [x] 5.3 Create basic views for other pages
    - Create HomeView for tap_new.html
    - Create StoreView for store.html
    - Create ContactView for contact.html
    - _Requirements: 1.4_

  - [x] 5.4 Configure URL patterns
    - Create checkout/urls.py with app URL patterns
    - Update src/urls.py to include checkout app URLs
    - Set up URL names for template linking
    - _Requirements: 1.4, 5.5_

- [x] 6. Configure Django admin interface
  - [x] 6.1 Register models in admin
    - Register CheckoutSubmission model in admin
    - Register SocialMediaLink model in admin
    - Configure admin display options for better usability
    - _Requirements: 4.1, 4.2_

  - [x] 6.2 Customize admin interface
    - Add search functionality for orders by name, email
    - Add filtering options by subscription type and date
    - Display orders in chronological order (most recent first)
    - _Requirements: 4.3, 4.4_

  - [ ]* 6.3 Write unit tests for admin functionality
    - Test admin registration and display
    - Verify search and filtering capabilities
    - _Requirements: 4.1, 4.2_

- [ ] 7. Checkpoint - Test basic functionality
  - Ensure all tests pass, verify form submission and data persistence works, ask the user if questions arise.

- [ ] 8. Final integration and cleanup
  - [ ] 8.1 Update all template links and navigation
    - Update all href attributes to use Django URL patterns
    - Ensure all static file references use {% static %} tags
    - Test all page navigation and functionality
    - _Requirements: 5.5_

  - [ ] 8.2 Create requirements.txt and documentation
    - Generate requirements.txt with all dependencies
    - Create basic setup instructions for local development
    - _Requirements: 1.2_

  - [ ]* 8.3 Write integration tests
    - End-to-end test for checkout form submission
    - Test template rendering and static file serving
    - Test admin interface functionality
    - _Requirements: All_

- [ ] 9. Final checkpoint - Complete system verification
  - Ensure all tests pass, verify all functionality works as expected, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation and user feedback
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation maintains existing visual design while adding Django backend functionality