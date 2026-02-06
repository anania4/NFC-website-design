from django.contrib import admin
from .models import CheckoutSubmission, SocialMediaLink


class SocialMediaLinkInline(admin.TabularInline):
    model = SocialMediaLink
    extra = 1
    fields = ('platform', 'url')


@admin.register(CheckoutSubmission)
class CheckoutSubmissionAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'subscription_type', 'amount', 'created_at')
    list_filter = ('subscription_type', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)  # Most recent first
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'title', 'email')
        }),
        ('Visual Identity', {
            'fields': ('profile_picture', 'company_logo'),
            'classes': ('collapse',)
        }),
        ('Subscription Details', {
            'fields': ('subscription_type', 'amount')
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
