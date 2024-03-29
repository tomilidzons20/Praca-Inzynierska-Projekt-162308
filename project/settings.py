import os
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2x(3v2-yy#4i9jie&a7+b+@tsu7gw8g1&jrh77=p+p2^uchs+%'

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
    'djmoney',
    'phonenumber_field',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'debug_toolbar',
    'ckeditor',
    'django_bleach',
    'formtools',
    'rosetta',

    # Local
    'car_rental.apps.CarRentalConfig',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DATABASE_NAME'),
        'USER': env.str('DATABASE_USER'),
        'PASSWORD': env.str('DATABASE_PASS'),
        'HOST': env.str('DATABASE_HOST'),
        'PORT': env.str('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('pl', _('Polish')),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'car_rental/locale/'),
]

TIME_ZONE = 'Poland'

USE_I18N = True

CURRENCIES = 'PLN'
CURRENCY_CHOICES = [('PLN', 'Polish Zloty')]

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR / 'static/'),
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_files/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_FORMS = {
    'login': 'accounts.forms.CustomLoginForm',
    'signup': 'accounts.forms.CustomSignupForm',
    'change_password': 'accounts.forms.CustomChangePasswordForm',
    'reset_password': 'accounts.forms.CustomResetPasswordForm',
    'add_email': 'accounts.forms.CustomEmailForm',
    'reset_password_from_key': 'accounts.forms.CustomResetPasswordKeyForm',
}

PHONENUMBER_DEFAULT_REGION = 'PL'

# Bleach

# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS = [
    'p', 'b', 'i', 'u', 'em',
    'strong', 'a', 's', 'h1',
    'h2', 'h3', 'h4', 'h5',
    'h6', 'pre', 'address',
    'img'
]

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = [
    'href', 'title', 'style', 'src',
    'alt',
]

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES = [
    'font-family', 'font-weight', 'text-decoration', 'font-variant',
    'color', 'background-color', 'height', 'width',
]

# Strip unknown tags
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = False

# Use the CKEditorWidget for bleached HTML fields
BLEACH_DEFAULT_WIDGET = 'ckeditor.widgets.CKEditorWidget'

MINIMUM_HOURS_BEFORE_RENT = 3
MINIMUM_RENT_HOURS = 1

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
