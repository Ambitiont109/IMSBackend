"""
ASGI config for anam_backend_main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

# from django.core.asgi import get_asgi_application
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anam_backend_main.settings")
django.setup()
application = get_default_application()

# origin setting
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anam_backend_main.settings')
# application = get_asgi_application()
