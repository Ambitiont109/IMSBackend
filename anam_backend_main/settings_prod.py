DEBUG = False
ALLOWED_HOSTS = ['3.136.224.87', 'standomsports.com']
# ALLOWED_HOSTS = ['192.232.213.37', 'standomsports.com']
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/IMSAdmin/static'
MEDIA_ROOT = '/var/www/IMSAdmin/upload'
# STATIC_ROOT = 'C:/Users/Ambition/Documents/standom/static'
# MEDIA_ROOT = 'C:/Users/Ambition/Documents/standom/static/upload'
MEDIA_URL = '/media/'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
print("Debug Flase")
