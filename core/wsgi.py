"""
WSGI config for core project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments.
"""

import os
from django.core.wsgi import get_wsgi_application

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Cria a aplicação WSGI
application = get_wsgi_application()