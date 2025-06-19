from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Secure secret key from environment
SECRET_KEY = os.environ.get('SECRET_KEY', 'unsafe-secret-key-for-dev-only')

# ✅ Toggle DEBUG from env (default False)
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# ✅ Allow Render host + localhost for dev
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# ✅ Installed Django + 3rd party + local apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'channels',
    'weather',
    'accounts',
]

# ✅ Essential middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skycast.urls'

# ✅ Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'weather', 'templates'),
            os.path.join(BASE_DIR, 'accounts', 'templates'),
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

# ✅ For HTTP and WebSocket support
WSGI_APPLICATION = 'skycast.wsgi.application'
ASGI_APPLICATION = 'skycast.asgi.application'

# ✅ Channels + Redis config (no SSL for Render)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [{
                "address": (os.environ.get('REDIS_HOST', '127.0.0.1'), 6379),
                "password": os.environ.get('REDIS_PASSWORD', ''),
                "ssl": False,  # ⛔ SSL breaks on free Render Redis
            }],
        },
    },
}

# ✅ PostgreSQL on Render, SQLite fallback for local
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ✅ Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ API Key
WEATHERSTACK_API_KEY = os.environ.get("WEATHERSTACK_API_KEY", "")

# ✅ Auth redirect
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/register/'
