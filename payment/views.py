from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
import stripe
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .models import Payment, PaymentHistory
#from datetime import timezone
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime, timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        amount = 1000  # Amount in cents (e.g., $10.00)
        
        try:
            # Create a PaymentIntent with the specified amount
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                metadata={"user_id": user.id}
            )

            # Save the payment instance
            payment = Payment.objects.create(
                user=user,
                amount=amount / 100,  # Convert cents to dollars
                currency="USD",
                stripe_payment_id=intent.id,
                status="pending"
            )

            return JsonResponse({"clientSecret": intent.client_secret})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

class CreateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        price_id = "price_23"  # Replace with your Stripe Price ID for the monthly plan

        # Create a new customer in Stripe if not already linked
        stripe_customer = stripe.Customer.create(email=user.email)

        # Create the subscription with a 7-day free trial
        subscription = stripe.Subscription.create(
            customer=stripe_customer.id,
            items=[{"price": price_id}],
            trial_period_days=7,
            metadata={"user_id": user.id}
        )

        # Save subscription in the database
        trial_end_date = timezone.now() + timezone.timedelta(days=7)
        Subscription.objects.create(
            user=user,
            stripe_subscription_id=subscription.id,
            trial_end_date=trial_end_date,
            is_active=True,
            status='active'
        )

        return Response({
            "subscription_id": subscription.id,
            "trial_end_date": trial_end_date
        })
    
class SubscriptionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        subscription = Subscription.objects.filter(user=user).first()

        if not subscription:
            return Response({"is_active": False, "message": "No subscription found."})

        # Check if trial or subscription is active
        if subscription.is_active and subscription.trial_end_date >= timezone.now():
            return Response({"is_active": True, "trial_end": subscription.trial_end_date})

        # If trial has ended, deactivate subscription
        subscription.is_active = False
        subscription.save()
        
        return Response({"is_active": False, "message": "Trial has ended, please subscribe."})   

def create_subscription_with_trial(user, payment_method_id):
    # Create a Stripe customer if not already existing
    customer = stripe.Customer.create(
        payment_method=payment_method_id,
        email=user.email,
        metadata={"user_id": user.id},
        invoice_settings={"default_payment_method": payment_method_id},
    )

    # Create the subscription with a 7-day trial
    stripe_subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[{"price": "23"}],
        trial_period_days=7,
        metadata={"user_id": user.id},
    )

    # Save subscription to database
    Subscription.objects.create(
        user=user,
        stripe_subscription_id=stripe_subscription.id,
        is_active=True,
        start_date=timezone.now(),
        status='active',
        trial_end_date=timezone.now() + timedelta(days=7),
    )

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'invoice.payment_succeeded':
        subscription_id = event['data']['object']['subscription']
        amount_paid = event['data']['object']['amount_paid'] / 100
        stripe_payment_id = event['data']['object']['id']
        
        stripe_subscription = stripe.Subscription.retrieve(subscription_id)
        user_id = stripe_subscription.metadata.get("user_id")
        user_subscription = Subscription.objects.filter(stripe_subscription_id=subscription_id, user_id=user_id).first()

        if user_subscription:
            # Update subscription and create payment history
            current_period_end = datetime.fromtimestamp(stripe_subscription.current_period_end)
            user_subscription.is_active = True
            user_subscription.status = 'active'
            user_subscription.end_date = current_period_end
            user_subscription.trial_end_date = None  # Trial has ended after the first payment
            user_subscription.save()

            PaymentHistory.objects.create(
                subscription=user_subscription,
                payment_date=timezone.now(),
                amount=amount_paid,
                stripe_payment_id=stripe_payment_id
            )

    elif event['type'] == 'invoice.payment_failed':
        # Handle payment failure
        subscription_id = event['data']['object']['subscription']
        stripe_subscription = stripe.Subscription.retrieve(subscription_id)
        user_id = stripe_subscription.metadata.get("user_id")
        user_subscription = Subscription.objects.filter(stripe_subscription_id=subscription_id, user_id=user_id).first()

        if user_subscription:
            user_subscription.is_active = False
            user_subscription.save()

    return HttpResponse(status=200)
