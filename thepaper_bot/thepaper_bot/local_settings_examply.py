DJANGO_BOT = {
    'WEBHOOK_HOST': "https://a.b.com",
    'WEBHOOK_PREFIX': "prefix/",
    'BOT_TOKEN': "", 
    'ALLOW_USER': [""],
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://Host:6379/0',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "pwd",
        },
    },
}
