#!/bin/bash

# THIẾT LẬP MẬT KHẨU TẠM THỜI
ADMIN_USERNAME="admin"
ADMIN_EMAIL="admin@example.com"

# 1. TẠO CƠ SỞ DỮ LIỆU
echo "Applying migrations..."
python manage.py migrate --noinput

# 2. TẠO VÀ ĐẶT MẬT KHẨU ADMIN (Sẽ dùng thuật toán MD5 từ settings.py)
echo "Creating admin user..."
# Lệnh tạo user không tương tác
python manage.py createsuperuser --noinput --username $ADMIN_USERNAME --email $ADMIN_EMAIL 2>/dev/null || true

echo "Setting admin password to 123456..."
# Lệnh đặt mật khẩu không tương tác
python manage.py changepassword $ADMIN_USERNAME --password 123456

# 3. THU THẬP STATIC FILES
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete. Starting Gunicorn..."