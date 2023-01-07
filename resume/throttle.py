from rest_framework.throttling import UserRateThrottle,BaseThrottle,SimpleRateThrottle
import time
from django.core.cache import cache 

# VISIT_RECORD = {}
# class EmployerCustomThrottle(BaseThrottle):

#     def __init__(self):
#         self.history = None   #Initialize access record
#         self.duration = 55
#         self.num_requests = 5


#     def allow_request(self, request, view):
#          """
#          Return `True` if the request should be allowed, `False` otherwise.
#          """
         
         
#          print("noo")
#          if request.user.is_authenticated:
#                 print(request.user.type)
#                 print(request.user.pro)
#                 if request.user.type=='EMPLOYER' and request.user.pro==False:
#                     return False
#                 else:
#                     return True
#          return True


#     def wait(self):
#         """
#         Optionally, return a recommended number of seconds to wait before
#         the next request.
#         """
#         cu_second = 55
#         return cu_second

        
# class BaseEmployerThrottle(UserRateThrottle):
#     scope = 'employer'

#     def parse_rate(self, rate):
#         if rate is None:
#             return None, None
#         num, period = rate.split('/')
#         num_requests = int(num)
#         duration = int(period)*86400
#         return num_requests, duration

class BaseEmployerThrottle2(UserRateThrottle):
    scope = 'employer2'
    
    
