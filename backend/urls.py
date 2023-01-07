from django.contrib import admin
from django.urls import include, path,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.documentation import include_docs_urls



schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('account/', include('allauth.urls'),name="socialaccount_signup"), # new
    path('resume/',include('resume.urls')),
    path('emp_profile/',include('employer_profile.urls')),
    path('urlShort/',include('urlShortner.urls')),
   #  path('elastic/',include('elastic.urls')),
    path('api_tracking/',include('api_tracking.urls')),
    path('pay/',include('stripe_payments.urls')),
    path('chat/',include('chat.urls')),
    path('search/',include('elastic.urls')),
    path('', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Todo Api')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # FOR TESTING SENTRY ISSUE TRACKER
    path('sentry-debug/', trigger_error),
    # path("api/auth/", include("dj_rest_auth.urls")),  # endpoints provided by dj-rest-auth
    # path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

]
# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]