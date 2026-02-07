from django.db import models
import uuid


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
