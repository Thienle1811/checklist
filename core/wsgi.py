"""
WSGI config for core project.
"""

import os

# Đảm bảo KHÔNG CÓ thư mục mẹ bị thêm vào path (sys.path.append)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()