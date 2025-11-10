import os
import sys
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# THÔNG TIN TÀI KHOẢN VÀ MẬT KHẨU MỚI
ADMIN_USERNAME = 'admin'
NEW_PASSWORD = 'MyFinalSecurePass2025!' # <--- MẬT KHẨU CỦA BẠN

try:
    # Lệnh này sẽ tạo tài khoản nếu nó không tồn tại VÀ đặt mật khẩu
    call_command('createsuperuser', username=ADMIN_USERNAME, email='admin@example.com', password=NEW_PASSWORD, interactive=False)
    print(f"Admin password set/reset successfully!")
except Exception as e:
    # Nếu tài khoản đã tồn tại, chúng ta sử dụng lệnh changepassword
    try:
        call_command('changepassword', ADMIN_USERNAME, password=NEW_PASSWORD)
        print(f"Admin password reset successfully (via changepassword).")
    except Exception as e:
        print(f"FATAL ERROR during admin setup: {e}")