#!/bin/bash

# THIẾT LẬP MẬT KHẨU TẠM THỜI
ADMIN_USERNAME="admin"
ADMIN_EMAIL="admin@example.com"
ADMIN_PASSWORD="123456" # Đặt mật khẩu đơn giản

# 1. TẠO CƠ SỞ DỮ LIỆU
echo "Applying migrations..."
python manage.py migrate --noinput

# 2. TẠO TÀI KHOẢN ADMIN (Không tương tác)
echo "Creating admin user..."
# Lệnh tạo user không tương tác
python manage.py createsuperuser --noinput --username $ADMIN_USERNAME --email $ADMIN_EMAIL 2>/dev/null || true

# 3. ĐẶT MẬT KHẨU BẰNG LỆNH CHANGEPASSWORD
# Lệnh này sẽ thành công vì:
# 1) Đã xóa AUTH_PASSWORD_VALIDATORS trong settings.py
# 2) Đã đặt PASSWORD_HASHERS là MD5 trong settings.py
echo "Setting admin password to 123456..."
python manage.py changepassword $ADMIN_USERNAME --password $ADMIN_PASSWORD

# 4. THU THẬP STATIC FILES
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete. Starting Gunicorn..."