from django.db import models
import uuid


class CardPricing(models.Model):
    """Model to manage card pricing from admin panel"""
    PLAN_TYPES = [
        ('individual', 'Individual Cards'),
        ('sm_business', 'S&M Business'),
        ('enterprise', 'Enterprise'),
        ('corporate', 'Corporate'),
    ]
    
    # plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    plan_type = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, help_text="Display name (e.g., 'Individual')")
    subtitle = models.CharField(max_length=200, help_text="Short description (e.g., 'Perfect for professionals')")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Birr")
    card_range = models.CharField(max_length=50, help_text="Number of cards (e.g., '1-9 Cards')")
    
    # Features (stored as text, one per line)
    features = models.TextField(
        help_text="Enter features, one per line (e.g., 'Customized Design')",
        default="Customized Design\n2 Year Subscription\nDigital Profile\nAnalytics Dashboard"
    )
    
    # Display options
    is_featured = models.BooleanField(default=False, help_text="Show 'Best Value' badge")
    is_popular = models.BooleanField(default=False, help_text="Show 'Most Popular' badge")
    display_order = models.IntegerField(default=0, help_text="Order to display (lower numbers first)")
    is_active = models.BooleanField(default=True, help_text="Show this plan on the website")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_features_list(self):
        """Return features as a list"""
        return [f.strip() for f in self.features.split('\n') if f.strip()]
    
    def __str__(self):
        return f"{self.name} - {self.price} Birr"
    
    class Meta:
        ordering = ['display_order', 'plan_type']
        verbose_name = 'Card Pricing'
        verbose_name_plural = 'Card Pricing'


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
    
    # Subscription Choice
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Chapa Payment Integration
    chapa_tx_ref = models.CharField(max_length=100, unique=True, null=True, blank=True)
    chapa_payment_status = models.CharField(max_length=50, default='pending')
    is_paid = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Generate unique transaction reference if not exists
        if not self.chapa_tx_ref:
            self.chapa_tx_ref = f"TAP-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subscription_type}"
    
    class Meta:
        ordering = ['-created_at']


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
    
    def __str__(self):
        return f"{self.submission.first_name} {self.submission.last_name} - {self.platform}"
    
    class Meta:
        unique_together = ['submission', 'platform']
