from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import requests
import json
from .models import CheckoutSubmission, SocialMediaLink
from .forms import CheckoutForm


class CheckoutView(View):
    """
    View to handle checkout form display and submission.
    GET: Display checkout form
    POST: Process form submission, save data, and redirect to Chapa payment
    """
    
    def get(self, request):
        """Display checkout form"""
        form = CheckoutForm()
        return render(request, 'checkout/checkout.html', {'form': form})
    
    def post(self, request):
        """Handle form submission and redirect to Chapa payment"""
        form = CheckoutForm(request.POST, request.FILES)
        
        print("📝 Form submitted")
        print(f"Form valid: {form.is_valid()}")
        
        if not form.is_valid():
            print(f"❌ Form errors: {form.errors}")
        
        if form.is_valid():
            try:
                print("✅ Form is valid, creating submission...")
                
                # Create checkout submission
                submission = CheckoutSubmission.objects.create(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    title=form.cleaned_data['title'],
                    email=form.cleaned_data['email'],
                    profile_picture=form.cleaned_data.get('profile_picture'),
                    company_logo=form.cleaned_data.get('company_logo'),
                    subscription_type=form.cleaned_data['subscription_type'],
                    amount=form.cleaned_data['amount'],
                    chapa_payment_status='pending'
                )
                
                print(f"✅ Submission created: ID={submission.id}, TX_REF={submission.chapa_tx_ref}")
                
                # Process social media links from POST data
                social_links = self._extract_social_links(request.POST)
                for platform, url in social_links.items():
                    if url.strip():  # Only create if URL is not empty
                        SocialMediaLink.objects.create(
                            submission=submission,
                            platform=platform.lower(),
                            url=url.strip()
                        )
                
                print(f"✅ Social links processed: {len(social_links)} links")
                
                # Initialize Chapa payment
                print("🔄 Initializing Chapa payment...")
                payment_url = self._initialize_chapa_payment(request, submission)
                
                if payment_url:
                    print(f"✅ Redirecting to: {payment_url}")
                    # Redirect to Chapa payment page
                    return redirect(payment_url)
                else:
                    print("❌ Payment URL is None")
                    messages.error(request, 'Unable to initialize payment. Please check server logs or configure Chapa API keys.')
                    return render(request, 'checkout/checkout.html', {'form': form})
                
            except Exception as e:
                # Handle any database or processing errors
                print(f"❌ Exception occurred: {str(e)}")
                import traceback
                traceback.print_exc()
                
                messages.error(
                    request, 
                    f'There was an error processing your order: {str(e)}'
                )
                return render(request, 'checkout/checkout.html', {'form': form})
        
        # Form is not valid - return with errors
        print("❌ Returning form with errors")
        return render(request, 'checkout/checkout.html', {'form': form})
    
    def _initialize_chapa_payment(self, request, submission):
        """Initialize Chapa payment and return checkout URL"""
        try:
            # Chapa API endpoint
            chapa_url = "https://api.chapa.co/v1/transaction/initialize"
            
            # Get Chapa secret key from settings
            chapa_secret_key = getattr(settings, 'CHAPA_SECRET_KEY', None)
            
            if not chapa_secret_key or chapa_secret_key == 'your-chapa-secret-key-here':
                print("⚠️ WARNING: CHAPA_SECRET_KEY not configured properly in settings")
                print("⚠️ For testing, redirecting to success page without payment")
                # For development/testing: redirect to success page directly
                messages.warning(
                    request,
                    'Payment gateway not configured. Order saved for testing purposes.'
                )
                submission.is_paid = False
                submission.chapa_payment_status = 'test_mode'
                submission.save()
                return request.build_absolute_uri(reverse('checkout_success', kwargs={'submission_id': submission.id}))
            
            # Prepare payment data
            payment_data = {
                "amount": str(submission.amount),
                "currency": "ETB",
                "email": submission.email,
                "first_name": submission.first_name,
                "last_name": submission.last_name,
                "tx_ref": submission.chapa_tx_ref,
                "callback_url": request.build_absolute_uri(reverse('payment_callback')),
                "return_url": request.build_absolute_uri(reverse('payment_callback')),
                "customization": {
                    "title": "TAP",  # Max 16 characters
                }
            }
            
            print(f"🔄 Initializing Chapa payment for TX_REF: {submission.chapa_tx_ref}")
            print(f"💰 Amount: {submission.amount} ETB")
            
            # Make request to Chapa API
            headers = {
                "Authorization": f"Bearer {chapa_secret_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(chapa_url, json=payment_data, headers=headers, timeout=10)
            
            print(f"📡 Chapa API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"✅ Chapa Response: {response_data}")
                
                if response_data.get('status') == 'success':
                    checkout_url = response_data.get('data', {}).get('checkout_url')
                    print(f"🔗 Checkout URL: {checkout_url}")
                    return checkout_url
            
            print(f"❌ Chapa API Error: {response.text}")
            return None
            
        except requests.exceptions.Timeout:
            print("⏱️ Chapa API request timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"🌐 Network error connecting to Chapa: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Error initializing Chapa payment: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
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


class PaymentCallbackView(View):
    """
    View to handle Chapa payment callback
    """
    
    def get(self, request):
        """Handle payment callback from Chapa"""
        tx_ref = request.GET.get('tx_ref')
        status = request.GET.get('status')
        
        if not tx_ref:
            messages.error(request, 'Invalid payment callback.')
            return redirect('checkout')
        
        try:
            submission = CheckoutSubmission.objects.get(chapa_tx_ref=tx_ref)
            
            # Verify payment with Chapa API
            if status == 'success':
                verified = self._verify_payment(tx_ref)
                
                if verified:
                    submission.is_paid = True
                    submission.chapa_payment_status = 'success'
                    submission.save()
                    
                    messages.success(
                        request,
                        f'Payment successful! Order #{submission.id} confirmed.'
                    )
                    return redirect('checkout_success', submission_id=submission.id)
            
            # Payment failed or cancelled
            submission.chapa_payment_status = 'failed'
            submission.save()
            
            messages.error(request, 'Payment was not completed. Please try again.')
            return redirect('checkout')
            
        except CheckoutSubmission.DoesNotExist:
            messages.error(request, 'Order not found.')
            return redirect('checkout')
    
    def _verify_payment(self, tx_ref):
        """Verify payment with Chapa API"""
        try:
            chapa_secret_key = getattr(settings, 'CHAPA_SECRET_KEY', None)
            
            if not chapa_secret_key:
                return False
            
            verify_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
            headers = {
                "Authorization": f"Bearer {chapa_secret_key}"
            }
            
            response = requests.get(verify_url, headers=headers)
            
            if response.status_code == 200:
                response_data = response.json()
                return response_data.get('status') == 'success'
            
            return False
            
        except Exception as e:
            print(f"Error verifying payment: {str(e)}")
            return False


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
    """View for card detail page"""
    
    def get(self, request):
        return render(request, 'card_detail.html')
