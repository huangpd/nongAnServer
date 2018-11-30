# coding=utf-8
"""
Django settings for naxy_api project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7u-xixlnfp49pj#r-k-z=8t$2!_f2(udi#jm9sicjhd&d&v@rr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'naxy_api.urls'

WSGI_APPLICATION = 'naxy_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'ccbd',  # 数据库名称
#         'USER': 'root',  # 数据库用户名
#         'PASSWORD': 'tianqi168',  # 数据库密码
#         'HOST': '',  # 数据库主机，留空默认为localhost
#         'PORT': '3306',  # 数据库端口
#     },
# }

DATABASES = {
     # 'default': {
     #    'ENGINE': 'django.db.backends.mysql',
     #    'NAME': 'ai_wenzhen',  # 数据库名称
     #    'USER': 'root',  # 数据库用户名
     #    'PASSWORD': '123',  # 数据库密码
     #    'HOST': 'localhost',  # 数据库主机，留空默认为localhost
     #    'PORT': '3306',  # 数据库端口
     # }
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            #'NAME': 'base_zhaopin',  # 数据库名称
            'NAME': 'db_naxy_enterprise',  # 数据库名称
            #'USER': 'root',  # 数据库用户名
            'USER': 'dev_naxy',  # 数据库用户名
            #'PASSWORD': 'hcmysql',  # 数据库密码
            'PASSWORD': 'rRxy!@&^131Naxy',  # 数据库密码
            'HOST': '47.96.162.131',  # 数据库主机，留空默认为localhost
            # 'HOST': '192.168.100.109',  # 数据库主机，留空默认为localhost
            'PORT': '3306',  # 数据库端口
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 设置True使用UTC时间，False为UTC+8的北京时间


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
