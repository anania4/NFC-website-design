# Design Document

## Overview

This design outlines the conversion of the existing static HTML checkout form to a Django-based backend that captures and persists the checkout form data with Chapa payment integration. The system will maintain the existing frontend design while adding Django backend functionality to store user submissions and process payments.

## Architecture

### Simple Django Structure

```
tap_django/
├── manage.py
├── requirements.txt
├── .env
├── tap_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── checkout/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/
│   └── checkout/
├── static/
└── media/
```

## Components and Interfaces

### Checkout Form Processing

**Models:**
- `CheckoutSubmission` - Store checkout form data
- `SocialMediaLink` - Store social media links

**Views:**
- `CheckoutView` - Display and process checkout form
- `PaymentCallbackView` - Handle Chapa payment callbacks

**Templates:**
- `checkout/checkout.html` - The existing checkout form

## Data Models

### Checkout Form Data

```python
# checkout/models.py
class CheckoutSubmission(models.Model):
    SUBSCRIPTION_TYPES = [
        ('individual', 'Individual Cards'),
        ('sm_business', 'S&M Business'),
        ('enterprise', 'Enterprise'),
        ('corporate', 'Corporate'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    email = models.EmailField()
    
    # Visual Identity
    profile_picture = models.ImageField(upload_to='profiles/pictures/', blank=True, null=True)
    company_logo = models.ImageField(upload_to='profiles/logos/', blank=True, null=True)
    
    # Links & Website
    personal_website = models.URLField(blank=True)
    
    # Subscription Choice
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Chapa Payment Integration
    chapa_tx_ref = models.CharField(max_length=100, unique=True)
    chapa_public_key = models.CharField(max_length=100)
    chapa_payment_status = models.CharField(max_length=50, default='pending')
    return_url = models.URLField()
    
    # Status
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter / X'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    submission = models.ForeignKey(CheckoutSubmission, related_name='social_links', on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    
    class Meta:
        unique_together = ['submission', 'platform']
```

## Form Processing

### Checkout Form Processing

```python
# checkout/views.py
class CheckoutView(View):
    def get(self, request):
        # Display checkout form
        return render(request, 'checkout/checkout.html')
    
    def post(self, request):
        form = CheckoutForm(request.POST, request.FILES)
        if form.is_valid():
            # Create checkout submission
            submission = CheckoutSubmission.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                title=form.cleaned_data['title'],
                email=form.cleaned_data['email'],
                profile_picture=form.cleaned_data.get('profile_picture'),
                company_logo=form.cleaned_data.get('company_logo'),
                personal_website=form.cleaned_data.get('personal_website'),
                subscription_type=form.cleaned_data['subscription_type'],
                amount=form.cleaned_data['amount'],
                chapa_tx_ref=generate_tx_ref(),
                chapa_public_key=settings.CHAPA_PUBLIC_KEY,
                return_url=request.build_absolute_uri(reverse('payment_callback')),
            )
            
            # Process social media links
            social_links = extract_social_links(request.POST)
            for platform, url in social_links.items():
                SocialMediaLink.objects.create(
                    submission=submission,
                    platform=platform,
                    url=url
                )
            
            # Redirect to Chapa payment
            return redirect_to_chapa_payment(submission)
        
        return render(request, 'checkout/checkout.html', {'form': form})

class PaymentCallbackView(View):
    def get(self, request):
        tx_ref = request.GET.get('tx_ref')
        status = request.GET.get('status')
        
        try:
            submission = CheckoutSubmission.objects.get(chapa_tx_ref=tx_ref)
            
            if status == 'success':
                # Verify payment with Chapa API
                if verify_chapa_payment(tx_ref):
                    submission.is_paid = True
                    submission.chapa_payment_status = 'success'
                    submission.save()
                    
                    return render(request, 'checkout/success.html', {'submission': submission})
            
            # Payment failed
            submission.chapa_payment_status = 'failed'
            submission.save()
            
            return render(request, 'checkout/failed.html', {'submission': submission})
            
        except CheckoutSubmission.DoesNotExist:
            return render(request, 'checkout/error.html')
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Checkout Form Data Persistence
*For any* valid checkout form submission, all form data should be stored in the database and retrievable with all original field values intact.
**Validates: Requirements 3.1**

### Property 2: Social Media Link Processing
*For any* checkout form with social media links, all provided social links should be created and associated with the correct checkout submission.
**Validates: Requirements 3.1**

### Property 3: File Upload Handling
*For any* checkout form with uploaded files (profile picture, company logo), the files should be stored securely and linked to the correct checkout submission.
**Validates: Requirements 10.5**

### Property 4: Payment Transaction Integrity
*For any* Chapa payment callback, the submission payment status should be updated correctly and either payment confirmation or failure should be processed completely.
**Validates: Requirements 4.2**

### Property 5: Transaction Reference Uniqueness
*For any* checkout submission, the generated Chapa transaction reference should be unique across all submissions in the system.
**Validates: Requirements 4.5**

### Property 6: Subscription Type and Amount Consistency
*For any* checkout submission, the amount should correctly correspond to the selected subscription type pricing.
**Validates: Requirements 4.1**

## Error Handling

### Form Validation Errors
- Invalid email formats → Clear validation messages
- Missing required fields → Field-specific error indicators
- Invalid file uploads → File type and size validation

### Payment Processing Errors
- Chapa API failures → Graceful error handling with retry options
- Invalid payment callbacks → Proper error logging and user notification
- Network timeouts → Fallback handling and status preservation

### File Upload Errors
- Invalid file types → Clear validation messages
- File size limits → Progress indication and size warnings
- Storage failures → Fallback handling and user notification

## Testing Strategy

### Unit Testing
- Model validation and data persistence
- Form validation and file upload handling
- Payment callback processing
- Social media link extraction and storage

### Property-Based Testing
- Checkout form submissions with various input combinations
- Payment processing with different callback scenarios
- File upload handling with various file types and sizes
- Social media link processing with different platform combinations

**Property Test Configuration:**
- Framework: Django's TestCase with hypothesis for property-based testing
- Minimum 100 iterations per property test
- Each test tagged with: **Feature: django-backend-conversion, Property {number}: {property_text}**

### Integration Testing
- End-to-end checkout form submission and payment processing
- File upload and storage functionality
- Chapa payment integration and callback handling
- Database integrity across different submission scenarios