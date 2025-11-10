import os
import sys
from django.core.management import call_command

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# THÔNG TIN TÀI KHOẢN VÀ MẬT KHẨU MỚI
ADMIN_USERNAME = 'admin'
NEW_PASSWORD = 'MyFinalSecurePass2025!' # <--- ĐẶT MẬT KHẨU CỦA BẠN VÀO ĐÂY

try:
    # Chạy lệnh changepassword của Django không tương tác
    call_command('changepassword', ADMIN_USERNAME, password=NEW_PASSWORD)
    print(f"Password for {ADMIN_USERNAME} reset successfully!")
except Exception as e:
    print(f"FATAL ERROR during password reset: {e}")