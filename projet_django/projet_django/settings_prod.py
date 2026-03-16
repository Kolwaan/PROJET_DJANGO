# settings_prod.py
# Hérite de settings.py et écrase uniquement ce qui change en production

import os
import dj_database_url
from .settings import *

# ─── SÉCURITÉ ──────────────────────────────────────────────────────────────────

SECRET_KEY = os.environ['SECRET_KEY']  # obligatoire, plante si absent

DEBUG = False

ALLOWED_HOSTS = [os.environ['RENDER_EXTERNAL_HOSTNAME']]  # fourni automatiquement par Render


# ─── BASE DE DONNÉES ───────────────────────────────────────────────────────────

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ['DATABASE_URL'],  # fourni automatiquement par Render
        conn_max_age=600,
    )
}


# ─── FICHIERS STATIQUES (whitenoise) ───────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # juste après SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ─── HEADERS DE SÉCURITÉ ───────────────────────────────────────────────────────

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

