from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
import threading



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        EmailMessage(
             subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        # EmailMessage(
        #     subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        # EmailThread(email).start()