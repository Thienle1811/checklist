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
# Logic: Mặc định là True (cho local). Chỉ False khi biến môi trường DEBUG được đặt rõ ràng là 'False'.
DEBUG = os.environ.get('DEBUG') != 'False'


# CẤU HÌNH ALLOWED_HOSTS
if DEBUG:
    # Cho phép tất cả host khi phát triển cục bộ
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.railway.app']
else:
    # Trong môi trường Production (DEBUG=False), cần host cho phép rõ ràng.
    # Lấy tên miền từ biến môi trường (nếu bạn có thêm domain custom)
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
    
    # Thêm domain mặc định của Railway
    if '.railway.app' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append('.railway.app')

    # Lọc bỏ các mục rỗng
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks', # Ứng dụng của bạn
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
# SỬ DỤNG LOGIC CHUYỂN ĐỔI: Nếu có biến môi trường DATABASE_URL (trên Railway) thì dùng PostgreSQL, nếu không (trên Local) thì dùng SQLite.
if os.environ.get('DATABASE_URL'):
    # Cấu hình cho PostgreSQL (Railway)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL')
        )
    }
else:
    # Cấu hình cho SQLite (Local)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'vi' 

TIME_ZONE = 'Asia/Ho_Chi_Minh' 

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# CẤU HÌNH STATIC FILES CHO PRODUCTION
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Redirect sau khi đăng nhập thành công
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
# THÊM CÁC CẤU HÌNH BẢO MẬT BẮT BUỘC CHO PRODUCTION/HTTPS (RAILWAY)

# 1. Báo cho Django biết rằng nó đang chạy sau một HTTPS proxy (Railway)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 2. Bắt buộc Django chỉ gửi cookie qua HTTPS (Bắt buộc cho CSRF/Session)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True