from rest_framework.permissions import BasePermission
from datetime import datetime
from .models import Subscription  # Adjust the import to match your models structure

class HasActiveSubscription(BasePermission):
    """
    Allows access only to users with an active subscription.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Retrieve the user’s subscription (assuming each user has only one active subscription)
        subscription = Subscription.objects.filter(user=request.user, status='active').first()

        # Check if the subscription exists and is still valid
        if subscription and subscription.end_date > datetime.now().date():
            return True

        return False