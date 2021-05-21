from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
]

AWS_ACCESS_KEY_ID = get_secret('AWS_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_KEY')
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'ilhwa-pharm'
AWS_S3_CUSTOM_DOMAIN = 's3.%s.amazonaws.com/%s' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)
AWS_S3_FILE_OVERWRITE = False
AWS_S3_0BJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = ''
STATIC_URL = 'http://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'config.s3media.MediaStorage'