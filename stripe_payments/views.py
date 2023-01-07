from urllib import response
from django.conf import settings
from django.shortcuts import render
import razorpay
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from stripe import Customer
from yaml import serialize
from .models import  SubscriptionDetails
from accounts.models import CustomUser
import time,pytz
# import datetime
from django.utils.timezone import make_aware
import stripe 
from datetime import datetime
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from . serializers import SubscriptionSerializer
from django.http import Http404, JsonResponse
from decouple import config
import json
from employer_profile.models import EmployerDetails
from rest_framework import status
# Create your views here.
# class RazorpaySubscription():
    # def __init__(self):
    #     self.api_key="rzp_test_aYqPyf8lIDNWWW"
    #     self.api_secret="OM3wVnCIrcpmSR7pPd5OuJ5Q"
def Client():
    # client=razorpay.Client(auth=("rzp_test_aYqPyf8lIDNWWW", "OM3wVnCIrcpmSR7pPd5OuJ5Q"))# appwharf
    api_key=config('RAZORPAY_API_KEY')
    secret_api_key=config('RAZORPAY_SECRET_API_KEY')
    client2=razorpay.Client(auth=(api_key,secret_api_key))
    # client2=razorpay.Client(auth=("rzp_test_UEbb04eC9SoOH6", "2mbVPLvfN7lx8BxnNkOaqvHR"))#my own 
    return client2 


@api_view(['POST'])
def create_subscriptions(request):
    
    user=request.user
    plan_id = request.data['plan_id']
    total_count=request.data['total_count']
    client=Client()
    sub=client.subscription.create({
    'plan_id': plan_id,
    # 'customer_notify': 1,
    # 'quantity': 5,
    'total_count': total_count,
    'notes': [user.email]
    # 'addons': [{'item': {'name': 'Delivery charges', 'amount': 30000,
    #            'currency': 'INR'}}],
     
    })

    data={
        'sub': sub
    }
 
    return Response(sub)
    
@csrf_exempt
@api_view(['GET','POST'])
@permission_classes([AllowAny])
def callback(request):
    # print(request.data)
    data1=request.data
    # print(data1["event"])
    date=datetime.today().strftime('%Y-%m-%d')

    if data1["event"]=="subscription.charged":
        email=data1["payload"]["payment"]["entity"]["email"]
        subscription_id=data1["payload"]["subscription"]["entity"]["id"]
        try:
           user_email_notes=data1["payload"]["subscription"]["entity"]["notes"][0]
        except:
           user_email_notes=""
        # print(user_email_notes)
        payment_method=data1["payload"]["payment"]["entity"]["method"]
        card_id=data1["payload"]["payment"]["entity"]["card"]["id"]
        card_type=data1["payload"]["payment"]["entity"]["card"]["type"]
        card_network=data1["payload"]["payment"]["entity"]["card"]["network"]
        card_last_4=data1["payload"]["payment"]["entity"]["card"]["last4"]
        card_name=data1["payload"]["payment"]["entity"]["card"]["name"]
        card_expiry_month=data1["payload"]["payment"]["entity"]["card"]["expiry_month"]
        card_expiry_year=data1["payload"]["payment"]["entity"]["card"]["expiry_year"]
        invoice_id=data1["payload"]["payment"]["entity"]["invoice_id"]
        customer_id=data1["payload"]["subscription"]["entity"]["customer_id"]
        status=data1["payload"]["subscription"]["entity"]["status"]
        period_start1=data1["payload"]["subscription"]["entity"]["current_start"]
        period_end1=data1["payload"]["subscription"]["entity"]["current_end"]
        mobile=data1["payload"]["payment"]["entity"]["contact"]
        plan_id=data1["payload"]["subscription"]["entity"]["plan_id"]
        period_start=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(period_start1))#make_aware(datetime.utcfromtimestamp(period_start1))#datetime.datetime.fromtimestamp(period_start1)
        period_end=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(period_end1))#make_aware(datetime.utcfromtimestamp(period_end1))#datetime.datetime.fromtimestamp(period_end1)
        # print(period_start)
        # print(period_end)
        try:
           user1=CustomUser.objects.get(email=user_email_notes)
        except CustomUser.DoesNotExist:
           user1 = None

        if user1:
            try:
               subb=SubscriptionDetails.objects.get(subscription_id=subscription_id)
            except SubscriptionDetails.DoesNotExist:
               subb = None
            if subb:
                if subb.user==None:
                    # subb.user=user1
                    SubscriptionDetails.objects.filter(subscription_id=subscription_id).update(
                            user=user1,
                            status=status,
                            period_start=period_start,
                            period_end=period_end,
                            plan_id=plan_id,
                            # billing_frequency=billing_frequency,
                            # plan_type=plan_type,
                            # plan_name=plan_type,
                            updated_at=date
                    )
                
                SubscriptionDetails.objects.filter(subscription_id=subscription_id).update(
                            status=status,
                            period_start=period_start,
                            period_end=period_end,
                            plan_id=plan_id,
                            # billing_frequency=billing_frequency,
                            # plan_type=plan_type,
                            # plan_name=plan_type,
                            updated_at=date
                        )
            else:
                SubscriptionDetails.objects.create(
                user=user1,
                email=email,
                payment_method=payment_method,
                card_id=card_id,
                card_type=card_type,
                card_network=card_network,
                card_expiry_month=card_expiry_month,
                card_expiry_year=card_expiry_year,
                card_last_4=card_last_4,
                invoice_id=invoice_id,
                card_name=card_name,
                payment_gateway="Razorpay",
                subscription_id= subscription_id,
                customer_id= customer_id,
                plan_id=plan_id,
                period_start=period_start,
                period_end=period_end,
                status=status, 
                created_at=date          
                    )
        else:
            try:
               subb=SubscriptionDetails.objects.get(subscription_id=subscription_id)
            except SubscriptionDetails.DoesNotExist:
               subb = None
            if subb==None:
                SubscriptionDetails.objects.create(
                    user=user1,
                    email=email,
                    payment_method=payment_method,
                    card_id=card_id,
                    card_type=card_type,
                    card_network=card_network,
                    card_expiry_month=card_expiry_month,
                    card_expiry_year=card_expiry_year,
                    card_last_4=card_last_4,
                    invoice_id=invoice_id,
                    card_name=card_name,
                    payment_gateway="Razorpay",
                    subscription_id= subscription_id,
                    customer_id= customer_id,
                    plan_id=plan_id,
                    period_start=period_start,
                    period_end=period_end,
                    status=status, 
                    created_at=date          
                        )
            else:
                # print(subb.user)
                subb.status=status
                subb.period_start=period_start
                subb.period_end=period_end
                subb.updated_at=date
                subb.update()

    data={
    }
    return Response(data)

import time

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    endpoint_secret=config('STRIPE_WEBHOOK_ENDPOINT_SECRET_KEY')
    payload=request.body
    event=json.loads(payload)
    date=datetime.today().strftime('%Y-%m-%d')
    
    # sig_header=request.META['HTTP_STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload=request.body,
            sig_header=request.META['HTTP_STRIPE_SIGNATURE'],
            secret=endpoint_secret
            #payload,sig_header,endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
    # print(event['type'])
    
    if event['type']=="customer.subscription.updated":
            # print("11111111111111")
            # print(event)
            subscription_id = event["data"]["object"]["id"]
            customer_id = event["data"]["object"]["customer"]
            period_start1 = event["data"]["object"]["current_period_start"]
            period_end1 = event["data"]["object"]["current_period_end"]
            status = event["data"]["object"]["status"]
            plan_id = event["data"]["object"]["plan"]["id"]
            amount = event["data"]["object"]["plan"]["amount"]
            # print(subscription_id)
            period_end=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(period_end1))
            period_start=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(period_start1))
            cancel_at_period_end=event["data"]["object"]["cancel_at_period_end"]
            cancel_at_date1=event["data"]["object"]["cancel_at"]
            if cancel_at_date1:
                cancel_at_date=time.strftime('%Y-%m-%d', time.localtime(cancel_at_date1))
            
            # print(period_end)
            # print(period_start)
            invoice_id= event["data"]["object"]["latest_invoice"]
        
            stripe.api_key = config('STRIPE_SECRET_KEY')

            invoice= stripe.Invoice.retrieve(
             invoice_id,
            )
            invoice_dict=stripe.util.convert_to_dict(invoice)
            invoice_pdf = invoice_dict["invoice_pdf"]
            payment_status = invoice_dict["status"] 

            # GET THE CHARGE RESPONSE LIKE CARD DETAILS
            if invoice_dict["charge"]:
                    charge=stripe.Charge.retrieve(
                        invoice_dict["charge"],
                    )
                    charge_dict=stripe.util.convert_to_dict(charge)
                    card_last4 = charge_dict["payment_method_details"]["card"]["last4"]
                    payment_method = charge_dict["payment_method_details"]["type"]
                    card_type = charge_dict["payment_method_details"]["card"]["funding"]
                    card_network = charge_dict["payment_method_details"]["card"]["network"]
                    card_expiry_month = charge_dict["payment_method_details"]["card"]["exp_month"]
                    card_expiry_year = charge_dict["payment_method_details"]["card"]["exp_year"]
            

            product_id=event["data"]["object"]["plan"]["product"]
            # plan_type=event["data"]["object"]["payment_settings"]["payment_method_options"]["card"]["mandate_options"]["description"]
            billing_frequency=event["data"]["object"]["plan"]["interval"]
            # if invoice_dict["charge"]:

            product=stripe.Product.retrieve(product_id)
            product_dict=stripe.util.convert_to_dict(product)

            plan_type=product_dict["name"]
            # print(plan_type)
                      
            try:
                subb=SubscriptionDetails.objects.get(subscription_id=subscription_id)
            except :
                subb = None

            if subb==None:
                if invoice_dict["status"]=="paid":
                    # SAVE NEW SUBSCRIPTION/PAYMENT DATA AND DETAILS
                    # print("222222222222222222222")

                    invoice_pdf = invoice_dict["invoice_pdf"]
                    payment_status = invoice_dict["status"] 
                    email= invoice_dict["customer_email"]
                    # p=stripe.Product.retrieve(invoice_id)

    
                    try:
                        user1=CustomUser.objects.get(email=email)
                    except:
                        user1 = None
                    # print("33333333333333333333")

                    SubscriptionDetails.objects.create(
                            user=user1,
                            email=email,
                            payment_method=payment_method,
                            card_type=card_type,
                            card_network=card_network,
                            card_expiry_month=card_expiry_month,
                            card_expiry_year=card_expiry_year,
                            card_last_4=card_last4,
                            invoice_id=invoice_id,
                            invoice_pdf=invoice_pdf,
                            payment_gateway="Stripe",
                            subscription_id= subscription_id,
                            customer_id= customer_id,
                            plan_id=plan_id,
                            billing_frequency=billing_frequency,
                            plan_type=plan_type,
                            plan_name=plan_type,
                            period_start=period_start,
                            period_end=period_end,
                            status=status, 
                            amount=amount,
                            payment_status=payment_status,
                            created_at=date          
                        )
                    EmployerDetails.objects.filter(user=user1).update(sub_plan=plan_type.upper(),current_subscription_id=subscription_id)
            else:
                # UPDATE ALL SUBSCRIPTION/PAYMENT DATA  AND DETAILS
                # print("inside====8")
                # print(invoice_pdf)
                SubscriptionDetails.objects.filter(subscription_id=subscription_id).update(
                status=status,
                period_start=period_start,
                period_end=period_end,
                plan_id=plan_id,
                billing_frequency=billing_frequency,
                invoice_id=invoice_id,
                invoice_pdf=invoice_pdf,
                plan_type=plan_type,
                plan_name=plan_type,
                updated_at=date
                )

                EmployerDetails.objects.filter(user=subb.user).update(sub_plan=plan_type.upper(),current_subscription_id=subscription_id)

    if event['type']=="invoice.payment_succeeded":
        # print("inside====9")
        # print(event)
        subscription_id = event["data"]["object"]["lines"][0]["subscription"]
        # print(subscription_id)
        invoice_id=event["data"]["object"]["id"]
        billing_reason=event["data"]["object"]["billing_reason"]
        invoice_pdf=event["data"]["object"]["invoice_pdf"]
        # print(invoice_pdf)
        
        SubscriptionDetails.objects.filter(subscription_id=subscription_id).update(
            invoice_id=invoice_id,
            invoice_pdf=invoice_pdf,
            billing_reason=billing_reason
        )
    
    if event['type']=="customer.subscription.deleted":
        
        subscription_id = event["data"]["object"]["id"]
        period_start1 = event["data"]["object"]["current_period_start"]
        period_end1 = event["data"]["object"]["current_period_end"]
        status = event["data"]["object"]["status"]
        plan_id = event["data"]["object"]["plan"]["id"]
        amount = event["data"]["object"]["plan"]["amount"]

        try:
                subb=SubscriptionDetails.objects.get(subscription_id=subscription_id)
        except :
                subb = None

        if subb:
            SubscriptionDetails.objects.filter(subscription_id=subscription_id).update(
                status=status,
                period_start=period_start,
                period_end=period_end,
                # plan_id=plan_id,
                # billing_frequency=billing_frequency,
                # plan_type=plan_type,
                # plan_name=plan_type,
                updated_at=date
                )
            EmployerDetails.objects.filter(user=subb.user).update(sub_plan="FREE")

            
           
    data1={

    }
    return Response(data1)

@api_view(['GET'])
def get_current_subscription_for_user(request):
    if request.user.is_authenticated:
        user=request.user
        try:
            queryset=SubscriptionDetails.objects.filter(user=user).latest('created_at')
            serialize=SubscriptionSerializer(queryset)
            return Response(serialize.data)
        except:
            queryset=None
        
        return Response({"error":"not-subscribed or subscription expired"},status=status.HTTP_404_NOT_FOUND)
    else:
        raise Http404

@api_view(['GET'])
def GetAllSubscriptions_for_currentuser(request):
    if request.user.is_authenticated:
        user=request.user
        try:
            queryset=SubscriptionDetails.objects.filter(user=user).order_by('-created_at')
            if queryset:
                serialize=SubscriptionSerializer(queryset,many=True)
                return Response(serialize.data)
            else:
                return Response({"error":"Not Subscribed Yet"},status=status.HTTP_404_NOT_FOUND)
        except:
            queryset=None
        
        return Response({"error":"not-subscribed or subscription expired"},status=status.HTTP_404_NOT_FOUND)
    else:
        raise Http404
 

@csrf_exempt
@api_view(["POST"])
# @permission_classes([AllowAny])
def UpgradeStripeSubscription(request):
    subscription_id = request.data['sub_id']
    price_id = request.data['price_id']

    try:
        stripe.api_key = config('STRIPE_SECRET_KEY')

        import time
        proration_date = int(time.time())

        subscription = stripe.Subscription.retrieve(subscription_id)
        sub=stripe.Subscription.modify(
                        subscription_id,
                        cancel_at_period_end=False,
                        proration_behavior='always_invoice', #create_prorations',
                        billing_cycle_anchor='now',
                        items=[{
                            'id': subscription['items']['data'][0].id,
                            'price': price_id,
                            # 'price_data':{
                            #     'product':"prod_Lx9n5Z6KVI0ymR",
                            # }
                        }]
                )
        # print(sub)
    except:
        pass
    
    return Response(status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
# @permission_classes([AllowAny])
def CancelStripeSubscription(request):
    subscription_id = request.data['sub_id']
    date=datetime.today().strftime('%Y-%m-%d')
    # cancel_at_period_end = request.data['cancel_at_period_end']
    try:
            stripe.api_key = config('STRIPE_SECRET_KEY')

            res=stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            res_dict=stripe.util.convert_to_dict(res)
            cancel_at_period_end1=res_dict["cancel_at_period_end"]
            cancel_at1=res_dict["cancel_at"]
            if cancel_at1:
                    cancel_at=time.strftime('%Y-%m-%d', time.localtime(cancel_at1))
            
            try:
                    subb=SubscriptionDetails.objects.get(subscription_id=subscription_id)
            except :
                    subb = None

            if subb:
                if cancel_at1 and cancel_at_period_end1:
                        SubscriptionDetails.objects.filter(subscription_id=subscription_id).update(
                            cancel_at_period_end=cancel_at_period_end1,
                            cancel_at=cancel_at,
                            updated_at=date
                        )

            return Response(status=status.HTTP_200_OK)
    except:
            pass
    return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
# @api_view(["POST"])
def get_Stripe_Invoice(request):
    if request.method=='POST':
        # print(list(request.POST.items()))
        invoice_id = request.POST['id']#request.POST.get("id", "") #
        # print(invoice_id)
        
        stripe.api_key = config('STRIPE_SECRET_KEY')

        invoice= stripe.Invoice.retrieve(
            invoice_id,
        )
        invoice_dict=stripe.util.convert_to_dict(invoice)
        return JsonResponse(invoice_dict)
