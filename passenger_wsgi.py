# This wasthe default behavior from the cpanel passenger_wsgi.py,
# we're overridding with the django wsgi below.
#
# import imp
# import sys
# sys.path.insert(0, os.path.dirname(__file__))
# wsgi = imp.load_source('wsgi', 'serve.py')
# application = wsgi.application

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_brasileiro.settings')

application = get_wsgi_application()