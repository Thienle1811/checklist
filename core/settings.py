"""
Django settings for core project.
"""

from pathlib import Path
import os
import dj_database_url # Cần cài đặt cục bộ: pip install dj-database-url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-z!$690#^1234567890') 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') != 'False'


# CẤU HÌNH ALLOWED_HOSTS
if DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.railway.app']
else:
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
    if '.railway.app' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append('.railway.app')
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Giữ lại AuthenticationMiddleware cho Admin Panel hoạt động
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL')
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation (Giữ lại cho Admin)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'vi' 
TIME_ZONE = 'Asia/Ho_Chi_Minh' 
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# XÓA CÁC CẤU HÌNH CHUYỂN HƯỚNG ĐĂNG NHẬP

# CẤU HÌNH BẢO MẬT BẮT BUỘC CHO PRODUCTION/HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


# =======================================================
# !!! CẤU HÌNH TẠM THỜI ĐỂ ĐẶT MẬT KHẨU ADMIN (BẮT BUỘC)
# !!! HÃY XÓA KHỐI NÀY SAU KHI ĐĂNG NHẬP ADMIN THÀNH CÔNG
# =======================================================
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]