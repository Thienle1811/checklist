#!/bin/bash

# THIẾT LẬP MẬT KHẨU TẠI ĐÂY
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="MyNewSecurePass456!" # <--- THAY ĐỔI MẬT KHẨU NÀY
ADMIN_EMAIL="admin@example.com"

# 1. TẠO CƠ SỞ DỮ LIỆU
echo "Applying migrations..."
python manage.py migrate --noinput

# 2. TẠO TÀI KHOẢN ADMIN (Không tương tác)
echo "Creating superuser..."
python manage.py createsuperuser --noinput --username $ADMIN_USERNAME --email $ADMIN_EMAIL 2>/dev/null || true

# 3. ĐẶT MẬT KHẨU SỬ DỤNG LỆNH SHELL
echo "Setting password for $ADMIN_USERNAME..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='$ADMIN_USERNAME')
user.set_password('$ADMIN_PASSWORD')
user.save()
EOF

# 4. THU THẬP STATIC FILES
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete. Starting Gunicorn..."

# KẾT THÚC SCRIPT