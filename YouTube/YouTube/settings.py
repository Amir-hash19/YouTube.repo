from pathlib import Path
from datetime import timedelta



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1g3(^!71jb8^^qgt+8ciq01!d2g4lvz(c&7q_cte6n%=-h9!ao'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ads.apps.AdsConfig',
    'channle.apps.ChannleConfig',
    'comments_like.apps.CommentsLikeConfig',
    'notifications.apps.NotificationsConfig',
    'search.apps.SearchConfig',
    'user_managment.apps.UserManagmentConfig',
    'video.apps.VideoConfig',
    'rest_framework',
    'django_celery_beat',
    'rest_framework_simplejwt',
    'drf_yasg',
    'django_filters',
    'rest_framework_simplejwt.token_blacklist',
    'storages',
    'django_elasticsearch_dsl',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'YouTube.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'YouTube.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "youtube_db",
        "USER": "admin",
        "PASSWORD": "amir112233",
        "HOST": "localhost",
        "PORT": "5432",
    }

}







# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],

    'DEFAULT_THROTTLE_RATES': {
    'anon': '5/min',
    'signup': '3/min',
    'login': '2/min',
    "channel":"4/min"

    }
}



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
    "AUTH_HEADER_TYPES": ("Bearer", ),
}



MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


AUTH_USER_MODEL = "user_managment.UserAccount"



# import os
# MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN")






# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "sandbox.smtp.mailtrap.io"  # یا آدرس SMTP که Mailtrap داده
# EMAIL_HOST_USER = '954054bea74b6f'  # از Mailtrap بگیر
# EMAIL_HOST_PASSWORD = "05107d414a8c71"  # از Mailtrap بگیر
# EMAIL_PORT = 2525  # یا پورتی که Mailtrap داده
# EMAIL_USE_TLS = True  # معمولاً TLS فعال است



# # Looking to send emails in production? Check out our Email API/SMTP product!
# EMAIL_HOST = 'sandbox.smtp.mailtrap.io'



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",  # دیتابیس شماره 2
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # اختیاری: برای سریالایز کردن
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            # اختیاری: برای فشرده‌سازی
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        }
    }
}




ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://localhost:9200'
    },
}
