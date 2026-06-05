"""
WSGI config for slfbl project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slfbl.settings')

application = get_wsgi_application()

# Start scheduler
from slfbl_app.scheduler import start_scheduler
start_scheduler()