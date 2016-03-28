'''
Created on Mar 28, 2016

@author: jivan
'''

SECRET_KEY = 'Not important for testing'
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'hanzi_basics-test.sqlite3'
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'hanzi_basics',
)
