"""
WSGI config for core project.
"""

import os
import sys # Đảm bảo import

from pathlib import Path

from django.core.wsgi import get_wsgi_application

# THÊM LOGIC ĐƯỜNG DẪN CỐ ĐỊNH NÀY:
# Thêm thư mục gốc (checklist/) vào Python path.
# __file__ là core/wsgi.py, os.path.dirname(__file__) là core/, os.path.dirname(os.path.dirname(__file__)) là thư mục gốc.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()