from django import forms
from django.core.exceptions import ValidationError
from .models import CheckoutSubmission, SocialMediaLink


class CheckoutForm(forms.ModelForm):
    """
    Django form for handling checkout form submissions with validation
    for personal information, file uploads, and social media links.
    """
    
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
            'subscription_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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
            
            # Check if email already exists (excluding current instance if updating)
            existing_submission = CheckoutSubmission.objects.filter(email=email)
            if self.instance.pk:
                existing_submission = existing_submission.exclude(pk=self.instance.pk)
            
            if existing_submission.exists():
                raise ValidationError('A submission with this email already exists.')
        
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