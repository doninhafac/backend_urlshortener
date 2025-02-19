from pathlib import Path

import os

from django.contrib.messages import constants as messages

import firebase_admin
from firebase_admin import credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$2xkf+evkw!kf#_ncm6ojx1d^a#iyc3j3!drxg5k4!(ae0e$iv"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'rest_framework.authtoken',
    "corsheaders",
    'links',
    'forgotpassword',
    "registros",
    "autenticacao",
    "sistema",
    'beneficios',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'config.middleware.NoCacheMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    
]

ROOT_URLCONF = "config.urls"

#integra com o sistema de auth padrao do Django

AUTH_USER_MODEL = 'registros.Usuario'

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend', #backend de autenticacao padrao
    'registros.auth_backends.EmailUsernameBackend'
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "resources")], #define o caminho da pasta que tera os recursos
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'andressacaroline082011@gmail.com'  # Seu e-mail do Gmail
EMAIL_HOST_PASSWORD = 'kcvu mjtu zghn nllo'  # Sua senha do Gmail ou senha de aplicativo


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {

    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'db_encurtador',
    'USER': 'postgres',
    'PASSWORD': 'root',
    'HOST': 'localhost',
    'PORT': '5432',
    }
}

# Settings for messages

MESSAGE_TAGS = {

    messages.DEBUG: 'debug',

    messages.INFO: 'info',

    messages.SUCCESS: 'success',

    messages.WARNING: 'warning',

    messages.ERROR: 'danger',
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATICFILES_FINDERS = [

'django.contrib.staticfiles.finders.FileSystemFinder',

'django.contrib.staticfiles.finders.AppDirectoriesFinder',

]

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "resources/static/"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#Configurações de variáveis globais
NUMBER_GRID_PAGES = 20
NUMBER_GRID_MODAL = 20

CORS_ALLOW_ALL_ORIGINS = [
    'http://localhost:5173',
]

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

FRONTEND_URL = "http://localhost:"
DEFAULT_FROM_EMAIL = 'no-reply@seusite.com'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho para a chave privada do Firebase
FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, 'config/firebaseServiceAccount.json')

# Inicializar o Firebase
cred = credentials.Certificate(FIREBASE_ADMIN_CREDENTIAL)
firebase_admin.initialize_app(cred)