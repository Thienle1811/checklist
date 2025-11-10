#!/bin/bash

# TẠO CƠ SỞ DỮ LIỆU
echo "Applying migrations..."
python manage.py migrate --noinput

# TẠO TÀI KHOẢN ADMIN (Nếu chưa tồn tại)
# Lệnh này sẽ tạo superuser không tương tác (non-interactive) nếu chưa có.
# Bạn cần phải đặt SECRET_KEY và các biến khác trên Railway.
echo "Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

# THU THẬP STATIC FILES
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete. Starting Gunicorn..."

# KẾT THÚC SCRIPT