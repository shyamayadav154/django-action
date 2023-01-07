from django.urls import include, path
from .views import CancelStripeSubscription, GetAllSubscriptions_for_currentuser, UpgradeStripeSubscription, callback, create_subscriptions, get_Stripe_Invoice, get_current_subscription_for_user, stripe_webhook
urlpatterns = [
    path("stripe/", include("drf_stripe.urls")),
    path('razorpay/subscription/create/', create_subscriptions, name="create_subs" ),
    path('razorpay/webhook/', callback, name="webhook"),
    path('stripe_pay/webhook/', stripe_webhook, name="webhook"),
    path('get_current_sub/', get_current_subscription_for_user, name="get_sub"),
    path('getAllSubs/', GetAllSubscriptions_for_currentuser, name="get_allsub"),
    path('getStripeInvoice/', get_Stripe_Invoice, name="get_invoice"),
    path('upgradeStripe/', UpgradeStripeSubscription, name="upgrade_stripe"),
    path('cancelStripe/', CancelStripeSubscription, name="cancel_stripe"),

]

# "ALL URLS UNDER pay/stripe"

# pay/ stripe/ my-subscription/
# pay/ stripe/ my-subscription-items/
# pay/ stripe/ subscribable-product/
# pay/ stripe/ checkout/
# pay/ stripe/ webhook/
# pay/ stripe/ customer-portal/