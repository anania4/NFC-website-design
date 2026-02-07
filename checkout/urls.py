from django.urls import path
from . import views

urlpatterns = [
    # Checkout URLs
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/success/<int:submission_id>/', views.CheckoutSuccessView.as_view(), name='checkout_success'),
    path('payment/callback/', views.PaymentCallbackView.as_view(), name='payment_callback'),
    
    # Main site URLs
    path('', views.HomeView.as_view(), name='home'),
    path('store/', views.StoreView.as_view(), name='store'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('card-detail/', views.CardDetailView.as_view(), name='card_detail'),
]