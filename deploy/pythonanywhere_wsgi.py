# deploy/pythonanywhere_wsgi.py
#
# Paste this into the WSGI configuration file on PythonAnywhere
# (Web tab -> "WSGI configuration file" link), replacing everything there.
# Change USERNAME to your PythonAnywhere username.
import os
import sys

PROJECT_DIR = "/home/itsnitinjack/portfolio_2026"

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
