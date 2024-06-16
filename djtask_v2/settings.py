"""
Django settings for djtask_v2 project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bj857kgu#hzv8go4jsmn(bnjjdnsmd5%2#h-d$4pt%++(9!(47'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "public_app",
    "user_app",
    "task_app",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djtask_v2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'djtask_v2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

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

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = './media'
MEDIA_URL = "/media/"

# STATIC_ROOT = "./static"

# STATIC_ROOT = './static'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "media"), os.path.join(BASE_DIR, "static")]

CKEDITOR_UPLOAD_PATH = "media"

SIMPLEUI_LOGO = "/static/images/logo.png"
# 关闭右侧广告
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False

# 隐藏首页的快捷操作和最近动作
# SIMPLEUI_HOME_QUICK = False
# SIMPLEUI_HOME_ACTION = False

# 修改左侧菜单首页设置
# SIMPLEUI_HOME_PAGE = '/'  # 指向页面（十有八九失败)
# SIMPLEUI_HOME_TITLE = '欢迎你!' # 首页标题
SIMPLEUI_HOME_ICON = 'fa fa-code'  # 首页图标

# 设置右上角Home图标跳转链接，会以另外一个窗口打开
SIMPLEUI_INDEX = '/'

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
DATETIME_FORMAT = 'Y-n-j H:i:s'
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Token',
    'X-Token',
    'Sign',
    'action',
    'Scenic-Id',
    'Session-Id'
)

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ],
}
#
# LOGS_ROOT = os.path.join(BASE_DIR, "logs")
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     # 日志格式
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s [%(threadName)s:%(thread)s prototype] [%(name)s:%(lineno)s prototype] [%('
#                       'module)s:%(funcName)s] [%(levelname)s]- %(message)s '
#         },
#     },
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     # 用来定义具体处理日志的方式
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',  # 输出到控制台
#             'formatter': 'standard'
#         }
#
#     },
#     # 配置用那种handlers来处理日志
#     'loggers': {
#         'django.server': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False
#         },
#         'django.db': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False
#         },
#
#     }
# }
