"""
Django settings for jianguo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ws&+o#9psmsu^lq0(hbv7g2(ik2=(#a-2b3_^5sj#hs&$q8xz@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'jianguo',

    'allauth',
    'allauth.socialaccount',
    'allauth.account',
    'file_storage',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'jianguo.urls'

WSGI_APPLICATION = 'jianguo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jianguo',
        'USER': 'jianguo',
        'PASSWORD': 'jianguo',
        'HOST': ''
    },
}

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh_CN'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'publish/static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'file_storage.storages.DatabaseStorage'

PROFILE_SIZE = (140, 140)

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"

DEFAULT_AVATAR = '/static/images/profile-default.png'
