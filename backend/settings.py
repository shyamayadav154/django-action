from pathlib import Path
import datetime
from decouple import config
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


SECRET_KEY = 'a80@58k@y&by1-w^n6(5k^k=gaq^se9(9ocvx1()07ij38ph29'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'drf_multiple_model',
    'django.contrib.sites',

    # django-addons
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'rest_framework_serializer_field_permissions',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    #Social allauth login
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    "allauth.socialaccount.providers.github",
    # 'django_rest_passwordreset',
    
    # user added apps
    'accounts.apps.AccountsConfig',
    'resume',
    'api_tracking',
    "drf_stripe",
    'stripe_payments', 
    'employer_profile' ,
    'drf_yasg',
    'coreapi',
    # 'django_elasticsearch_dsl',
    # 'django_elasticsearch_dsl_drf',
    # 'elastic',
    'channels',
    'chat',
    'urlShortner',
    'anymail',
    # Django Elasticsearch integration
    'django_elasticsearch_dsl',
     
    # 'django_celery_results',
    # 'django_celery_beat',

    # Django REST framework Elasticsearch integration (this package)
    'django_elasticsearch_dsl_drf',
    'elastic',
   
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
 #   "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rest_framework_serializer_field_permissions.middleware.RequestMiddleware',

    

]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = 'backend.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'mrdb3',
             'USER': 'postgres',
             'PASSWORD': 'J8qG8NcjllagxkGj',
             'HOST': '34.131.209.100',
             'PORT': '5432',
             }
# }
    # 'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'postgres1',
        # 'USER': 'postgres',
        # 'PASSWORD': '123456',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5432',

        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'postgres',
        # 'USER': 'appuser',
        # 'PASSWORD': 'yav&cEMWk4mee_mW',
        # 'HOST': 'meresume.catirtpm8zdb.ap-south-1.rds.amazonaws.com',
        # 'PORT': '5432',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# Added by user
AUTH_USER_MODEL = 'accounts.CustomUser'



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "dj_rest_auth.utils.JWTCookieAuthentication",
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        # 'resume.throttle.BaseEmployerRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '5000/minute',
        'employer2': '1/day',# employer rate-limiting 
        # 'employer': '50/14', # 50=request  per 14=day
    },
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend','rest_framework.filters.SearchFilter'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}

CORS_ORIGIN_WHITELIST = ('https://mevvit.com', 'http://127.0.0.1:3000', 'http://localhost:3000','https://www.mevvit.com','https://dry.mevvit.com')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    # 'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}


REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserSerializer'
}


ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },

    'linkedin': {
        'SCOPE': [
            'r_basicprofile',
            'r_emailaddress'
        ],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url',
        ]
    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}


# # we are turning off email verification for now
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_REQUIRED = False

SITE_ID = 1  # https://dj-rest-auth.readthedocs.io/en/latest/installation.html#registration-optional
REST_USE_JWT = True  # use JSON Web Tokens

LOGIN_REDIRECT_URL="login"
AUTHENTICATION_BACKENDS = [
     # Needed to login by username in Django admin, regardless of `allauth`
     'django.contrib.auth.backends.ModelBackend',
     # `allauth` specific authentication methods, such as login by e-mail
     'allauth.account.auth_backends.AuthenticationBackend',
 ]

DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'

DRF_STRIPE = {
    "STRIPE_API_SECRET":config('STRIPE_SECRET_KEY'),
    "STRIPE_WEBHOOK_SECRET":config('STRIPE_WEBHOOK_SECRET') ,
    "FRONT_END_BASE_URL": "https://mevvit.com/",
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST =  'smtp.gmail.com' #'smtp.mailtrap.io' 
# EMAIL_HOST_USER = '' #'0ed99385d412cf'
# EMAIL_HOST_PASSWORD = ''  #'81bae8ae5e2806'
# EMAIL_PORT = 587

# EMAIL_HOST = "smtp-relay.sendinblue.com"  #'smtp.sendgrid.net'
# EMAIL_HOST_USER = "mevvit" #'apikey' # this is exactly the value 'apikey'
# EMAIL_HOST_PASSWORD =  "xsmtpsib-63d485e598de09f5694de1cfedc7e4624759c6814e2c9c09c13a9476863d134b-pMmUAfIwH2rKL6tX" #'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' # this is your API key
# EMAIL_PORT =  587 #587
# EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = 'anirbanchakraborty967@gmail.com' # this is the sendgrid email

# SENDGRID_API_KEY="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"
ELASTICSEARCH_DSL={
    'default': {
        "hosts": "34.131.132.42:9200",
        # 'hosts': "localhost:9200"#"localhost:9200"
    },
}

RESET_REDIRECT_URL="https://mevvit.com/reset-password/"

FRONTEND_BASE_URL="https://mevvit.com/"

EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"

ANYMAIL = {
    "SENDINBLUE_API_KEY": "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"
    # "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",
# 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
}

DEFAULT_FROM_EMAIL="Mevvit Team <team@mevvit.com>"


'''Setup your Celery Settings here'''

# Celery Configuration Options
CELERY_BROKER_URL = 'redis://127.0.0.1:6379' #'redis://34.131.31.155:9125' 
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER
task_serializer = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

#Sotres your tasks status in django database 
# CELERY_RESULT_BACKEND
result_backend = 'django-db'

#Celery beat Setting
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# CELERY_IMPORTS
imports = [
    'resume.tasks',
]


# FOR SENTRY CONFIGURATION
sentry_sdk.init(
    dsn="https://7fc42107ad1c419180d093d79aa5a630@o4504417782136832.ingest.sentry.io/4504417830567936",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)