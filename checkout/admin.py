from django.contrib import admin
from django.utils.html import format_html
from .models import CheckoutSubmission, SocialMediaLink


class SocialMediaLinkInline(admin.TabularInline):
    model = SocialMediaLink
    extra = 1
    fields = ('platform', 'url')


@admin.register(CheckoutSubmission)
class CheckoutSubmissionAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'subscription_type', 'amount', 'payment_status_badge', 'profile_picture_preview', 'created_at')
    list_filter = ('subscription_type', 'is_paid', 'chapa_payment_status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'chapa_tx_ref')
    readonly_fields = ('created_at', 'updated_at', 'chapa_tx_ref', 'profile_picture_preview_large', 'company_logo_preview_large')
    ordering = ('-created_at',)  # Most recent first
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'title', 'email')
        }),
        ('Visual Identity', {
            'fields': (
                'profile_picture', 
                'profile_picture_preview_large',
                'company_logo', 
                'company_logo_preview_large'
            ),
            'classes': ('collapse',)
        }),
        ('Subscription Details', {
            'fields': ('subscription_type', 'amount')
        }),
        ('Payment Information', {
            'fields': ('chapa_tx_ref', 'chapa_payment_status', 'is_paid'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [SocialMediaLinkInline]
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'first_name'
    
    def payment_status_badge(self, obj):
        """Display payment status with color coding"""
        if obj.is_paid:
            color = '#28a745'  # Green
            status = '✓ Paid'
        elif obj.chapa_payment_status == 'pending':
            color = '#ffc107'  # Yellow
            status = '⏳ Pending'
        else:
            color = '#dc3545'  # Red
            status = '✗ Failed'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{}</span>',
            color, status
        )
    payment_status_badge.short_description = 'Payment Status'
    
    def profile_picture_preview(self, obj):
        """Small preview for list view"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return "No Image"
    profile_picture_preview.short_description = 'Profile'
    
    def profile_picture_preview_large(self, obj):
        """Large preview for detail view"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.profile_picture.url
            )
        return "No profile picture uploaded"
    profile_picture_preview_large.short_description = 'Profile Picture Preview'
    
    def company_logo_preview_large(self, obj):
        """Large preview for detail view"""
        if obj.company_logo:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.company_logo.url
            )
        return "No company logo uploaded"
    company_logo_preview_large.short_description = 'Company Logo Preview'


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('get_submission_name', 'platform', 'url')
    list_filter = ('platform',)
    search_fields = ('submission__first_name', 'submission__last_name', 'submission__email', 'platform')
    ordering = ('submission', 'platform')
    
    def get_submission_name(self, obj):
        return f"{obj.submission.first_name} {obj.submission.last_name}"
    get_submission_name.short_description = 'Customer'
    get_submission_name.admin_order_field = 'submission__first_name'
