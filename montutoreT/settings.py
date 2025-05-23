"""
Django settings for montutoreT project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import pymysql
pymysql.install_as_MySQLdb()
import dotenv
dotenv.load_dotenv()

# Installation de MySQLdb via pymysql
pymysql.install_as_MySQLdb() 

import os
from pathlib import Path

from dotenv import load_dotenv


# Charger automatiquement les variables depuis un fichier .env (utile en dev)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Fichiers statiquespy manage.py collectstatic

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # Dossier où les fichiers statiques seront collectés en production


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$f02f4z9s)&cqzv#j6dz$=zr^eut5&^jg@ocwjjo86t*jc^o&&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'monprojet',
]

AUTH_USER_MODEL = 'monprojet.Utilisateur'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
]

ROOT_URLCONF = 'montutoreT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "monprojet" / "templates"],
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

WSGI_APPLICATION = 'montutoreT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

import os
import dj_database_url

# Production

DEBUG = os.getenv('DEBUG', 'False') == 'True'
# ALLOWED_HOSTS = ['restaurant-10-dxaw.onrender.com', 'localhost', '127.0.0.1']


# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True
    )
}


SECRET_KEY = os.getenv('SECRET_KEY')
# DEBUG = os.getenv('DEBUG') == 'True'
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'


LOGIN_REDIRECT_URL = 'monadmin'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Serveur SMTP de Gmail (ou autre)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'souadahmed2910@gmail.com'  # Remplace par ton email
EMAIL_HOST_PASSWORD = 'mdnj p eaj ngtd qwev'  # Remplace par ton mot de passe

CSRF_COOKIE_SECURE = True

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
]

import os

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
STATIC_URL = '/static/'  # pour l'URL de base des fichiers statiques
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Assurez-vous que ce chemin est correct
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'monprojet/static'),  # adapte le chemin
]
CSRF_USE_SESSIONS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'