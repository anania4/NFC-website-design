from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from .models import CheckoutSubmission, SocialMediaLink
from .forms import CheckoutForm


class CheckoutView(View):
    """
    View to handle checkout form display and submission.
    GET: Display checkout form
    POST: Process form submission and save data
    """
    
    def get(self, request):
        """Display checkout form"""
        form = CheckoutForm()
        return render(request, 'checkout/checkout.html', {'form': form})
    
    def post(self, request):
        """Handle form submission and validation"""
        form = CheckoutForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Create checkout submission
                submission = CheckoutSubmission.objects.create(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    title=form.cleaned_data['title'],
                    email=form.cleaned_data['email'],
                    profile_picture=form.cleaned_data.get('profile_picture'),
                    company_logo=form.cleaned_data.get('company_logo'),
                    subscription_type=form.cleaned_data['subscription_type'],
                    amount=form.cleaned_data['amount']
                )
                
                # Process social media links from POST data
                social_links = self._extract_social_links(request.POST)
                for platform, url in social_links.items():
                    if url.strip():  # Only create if URL is not empty
                        SocialMediaLink.objects.create(
                            submission=submission,
                            platform=platform.lower(),
                            url=url.strip()
                        )
                
                # Success message
                messages.success(
                    request, 
                    f'Thank you {submission.first_name}! Your order has been submitted successfully. '
                    f'Order ID: {submission.id}'
                )
                
                # Redirect to prevent form resubmission
                return redirect('checkout_success', submission_id=submission.id)
                
            except Exception as e:
                # Handle any database or processing errors
                messages.error(
                    request, 
                    'There was an error processing your order. Please try again.'
                )
                return render(request, 'checkout/checkout.html', {'form': form})
        
        # Form is not valid - return with errors
        return render(request, 'checkout/checkout.html', {'form': form})
    
    def _extract_social_links(self, post_data):
        """
        Extract social media links from POST data.
        Looks for fields like 'social_linkedin', 'social_twitter', etc.
        """
        social_links = {}
        
        # Map of form field names to model platform choices
        platform_mapping = {
            'social_linkedin': 'linkedin',
            'social_twitter': 'twitter',
            'social_instagram': 'instagram',
            'social_facebook': 'facebook',
            'social_tiktok': 'tiktok',
            'social_telegram': 'telegram',
            'social_whatsapp': 'whatsapp'
        }
        
        for field_name, platform in platform_mapping.items():
            url = post_data.get(field_name, '').strip()
            if url:
                social_links[platform] = url
        
        return social_links


class CheckoutSuccessView(View):
    """
    View to display checkout success page
    """
    
    def get(self, request, submission_id):
        """Display success page with submission details"""
        try:
            submission = CheckoutSubmission.objects.get(id=submission_id)
            return render(request, 'checkout/success.html', {'submission': submission})
        except CheckoutSubmission.DoesNotExist:
            messages.error(request, 'Order not found.')
            return redirect('checkout')


# Basic views for other pages
class HomeView(View):
    """View for the home page (tap_new.html)"""
    
    def get(self, request):
        return render(request, 'home.html')


class StoreView(View):
    """View for the store page"""
    
    def get(self, request):
        return render(request, 'store.html')


class ContactView(View):
    """View for the contact page"""
    
    def get(self, request):
        return render(request, 'contact.html')


class CardDetailView(View):
    """View for card detail page (redirects to checkout)"""
    
    def get(self, request):
        # For now, redirect to checkout since we don't have a separate card detail page
        return redirect('checkout')
