from django.shortcuts import render
from django.core.mail import send_mail,EmailMessage
from anymail.message import AnymailMessage
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework import mixins, viewsets,status
from rest_framework.permissions import AllowAny
from django.template import Template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string,get_template
from django.utils.html import strip_tags
from accounts.models import CustomUser
from django.core import mail


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def Email(request):
    data=request.data
    sender=request.data.get('from',None)
    email=request.data.get('email',None)
    message_body=request.data.get('message',None)
    to=request.data.get('receiver',None)
    subject=request.data.get('subject',None)

    # if request.user.type=="EMPLOYER" and request.user.email==sender :
    if request.user.is_authenticated:
        sender=sender
    else:
        sender=email
    try:
        rec_user=CustomUser.objects.get(email=to)
        rec_username=rec_user.first_name
    except:
        
        # if not rec_username:
            rec_username="Candidate"

    try:
        sender_user=CustomUser.objects.get(email=sender)
        sender_username=sender_user.first_name
    except:
    #     pass
    # if not sender_username:
        sender_username="Recruiter"

    if request.method == 'POST':
            
            context={"sender":sender,"message":message_body,"user":rec_username,"sender_user":sender_username,"subject":subject}
            html_body = render_to_string("employer_message.html",context)
            # t= get_template('employer_message.html').render(context)
            html_text = strip_tags(html_body)
            headers = {'Reply-To': sender}
            message = AnymailMessage(
               subject="[Mevvit]-Hi {user} , You've received direct message from {sender_user}".format(user=rec_username,sender_user=sender_username),
               body=html_body,
               to=[to],
               headers=headers,
               tags=["Urjent"],# Anymail extra in constructor
              )
            message.content_subtype = "html"
            message.send()

            # msg = EmailMultiAlternatives(subject="hello",from_email=settings.DEFAULT_FROM_EMAIL,
            #                             to=[to], body="HI You've received direct message from")
            # msg.attach_alternative(html_body, "text/html")
            # msg.send()
            # subject="TEST"
            # from_email=settings.DEFAULT_FROM_EMAIL
            # mail.send_mail(subject, html_text, from_email,[to], html_message=t)


            return JsonResponse({'message_status':"done",'status':200})

    else:
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED,data="Permission Denied",safe=False)




# merge_data = {
            #     'ORDERNO': "12345", 'TRACKINGNO': "1Z987"
            # }
            # subject = render_to_string("message_subject.txt", merge_data).strip()
            # text_body = render_to_string("message_body.txt", merge_data)
            # message.template_id = 3   # use this Sendinblue template
            # message.from_email = None  # to use the template's default sender
            # statu = message.anymail_status  # available after sending
            # statu.message_id  # e.g., '<12345.67890@example.com>'
            # stat=statu.recipients[to].status  # e.g., 'queued'
            # msg = EmailMultiAlternatives(subject="hello",from_email=settings.DEFAULT_FROM_EMAIL,
            #                             to=[to], body=html_body)
            # msg.attach_alternative(html_body, "text/html")
            # msg.send()
# send_mail('SENDINBLUE','HELLO', 'anirbanchakraborty967@gmail.com',['anirbanchakraborty714@gmail.com'])









