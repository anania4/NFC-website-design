from django import forms
from django.core.exceptions import ValidationError
from .models import CheckoutSubmission, SocialMediaLink


class CheckoutForm(forms.ModelForm):
    """
    Django form for handling checkout form submissions with validation
    for personal information, file uploads, and social media links.
    """
    
    # Override subscription_type to use ChoiceField instead of ModelChoiceField
    subscription_type = forms.ChoiceField(
        choices=[],  # Will be populated in __init__
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    # Additional field for personal website (not in model but in HTML form)
    personal_website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://yourwebsite.com',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = CheckoutSubmission
        fields = [
            'first_name', 
            'last_name', 
            'title', 
            'email',
            'profile_picture',
            'company_logo',
            'subscription_type',
            'amount'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Anania',
                'class': 'form-control',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Minda',
                'class': 'form-control',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. CEO',
                'class': 'form-control',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'e.g. user@example.com',
                'class': 'form-control',
                'required': True
            }),
            'profile_picture': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'form-control'
            }),
            'company_logo': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically populate subscription_type choices from CardPricing
        from .models import CardPricing
        from django.core.cache import cache
        
        # Get pricing plans from cache
        cache_key = 'active_pricing_plans'
        pricing_plans = cache.get(cache_key)
        
        if pricing_plans is None:
            # Cache miss - fetch from database
            pricing_plans = list(CardPricing.objects.filter(is_active=True).order_by('display_order'))
            cache.set(cache_key, pricing_plans, 3600)
        
        # Build choices from pricing plans
        subscription_choices = [('', 'Choose a subscription type...')]  # Empty choice
        subscription_choices.extend([
            (plan.plan_type, plan.name) for plan in pricing_plans
        ])
        
        # Update the subscription_type field choices
        self.fields['subscription_type'].choices = subscription_choices
        
        # Make certain fields required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['title'].required = True
        self.fields['email'].required = True
        self.fields['subscription_type'].required = True
        self.fields['amount'].required = True
        
        # Set field labels to match the HTML form
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['title'].label = 'Title'
        self.fields['email'].label = 'Email'
        self.fields['profile_picture'].label = 'Profile Picture'
        self.fields['company_logo'].label = 'Company Logo'
        self.fields['subscription_type'].label = 'Subscription Type'
        self.fields['amount'].label = 'Amount'
        self.fields['personal_website'].label = 'Personal Website / Link'
    
    def clean_profile_picture(self):
        """Validate profile picture file upload"""
        profile_picture = self.cleaned_data.get('profile_picture')
        
        if profile_picture:
            # Check file size (limit to 5MB)
            if profile_picture.size > 5 * 1024 * 1024:
                raise ValidationError('Profile picture file size must be less than 5MB.')
            
            # Check file type
            if not profile_picture.content_type.startswith('image/'):
                raise ValidationError('Profile picture must be an image file.')
        
        return profile_picture
    
    def clean_company_logo(self):
        """Validate company logo file upload"""
        company_logo = self.cleaned_data.get('company_logo')
        
        if company_logo:
            # Check file size (limit to 5MB)
            if company_logo.size > 5 * 1024 * 1024:
                raise ValidationError('Company logo file size must be less than 5MB.')
            
            # Check file type
            if not company_logo.content_type.startswith('image/'):
                raise ValidationError('Company logo must be an image file.')
        
        return company_logo
    
    def clean_amount(self):
        """Validate amount is positive"""
        amount = self.cleaned_data.get('amount')
        
        if amount is not None and amount <= 0:
            raise ValidationError('Amount must be greater than zero.')
        
        return amount
    
    def clean_email(self):
        """Validate email format and uniqueness"""
        email = self.cleaned_data.get('email')
        
        if email:
            # Convert to lowercase for consistency
            email = email.lower()
            
            # Check if email already exists with a successful payment
            # Allow retries if previous submissions failed or are still pending
            existing_paid_submission = CheckoutSubmission.objects.filter(
                email=email,
                is_paid=True
            )
            
            if self.instance.pk:
                existing_paid_submission = existing_paid_submission.exclude(pk=self.instance.pk)
            
            if existing_paid_submission.exists():
                raise ValidationError(
                    'A paid order with this email already exists. '
                    'Please contact support if you need assistance.'
                )
        
        return email


class SocialMediaLinkForm(forms.ModelForm):
    """
    Form for handling individual social media links
    """
    
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url']
        
        widgets = {
            'platform': forms.Select(attrs={
                'class': 'form-control'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'required': True
            })
        }
    
    def clean_url(self):
        """Validate social media URL format"""
        url = self.cleaned_data.get('url')
        platform = self.cleaned_data.get('platform')
        
        if url and platform:
            # Basic URL validation - ensure it's a proper URL
            if not url.startswith(('http://', 'https://')):
                raise ValidationError('URL must start with http:// or https://')
            
            # Platform-specific validation could be added here
            platform_domains = {
                'linkedin': ['linkedin.com'],
                'twitter': ['twitter.com', 'x.com'],
                'instagram': ['instagram.com'],
                'facebook': ['facebook.com'],
                'tiktok': ['tiktok.com'],
                'telegram': ['t.me', 'telegram.me'],
                'whatsapp': ['wa.me', 'whatsapp.com']
            }
            
            if platform in platform_domains:
                valid_domains = platform_domains[platform]
                if not any(domain in url.lower() for domain in valid_domains):
                    raise ValidationError(f'URL must be from a valid {platform} domain.')
        
        return url


# Formset for handling multiple social media links
SocialMediaLinkFormSet = forms.inlineformset_factory(
    CheckoutSubmission,
    SocialMediaLink,
    form=SocialMediaLinkForm,
    extra=0,  # No extra empty forms by default
    can_delete=True,
    min_num=0,
    validate_min=False
)