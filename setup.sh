#!/bin/bash

# FILE NÀY CHỈ CHỨA LỆNH KHỞI TẠO DB/STATIC SAU KHI ADMIN ĐÃ ĐƯỢC XỬ LÝ

# 1. TẠO CƠ SỞ DỮ LIỆU
echo "Applying migrations..."
python manage.py migrate --noinput

# 2. THU THẬP STATIC FILES
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete. Starting Gunicorn..."