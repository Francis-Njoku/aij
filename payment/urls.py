from django.urls import path
from .views import stripe_webhook
from .views import CreateSubscriptionView, SubscriptionStatusView

urlpatterns = [
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create-subscription'),
    path('subscription-status/', SubscriptionStatusView.as_view(), name='subscription-status'),
]