import os
import django
import sys

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
django.setup()

from django.contrib.auth import get_user_model

# THÔNG TIN TÀI KHOẢN
NEW_PASSWORD = 'MyFinalSecurePass2025!' # <--- ĐẶT MẬT KHẨU MỚI (VÀ KHÁC LẦN TRƯỚC)
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@example.com'

User = get_user_model()

try:
    # 1. TÌM KIẾM HOẶC TẠO MỚI ADMIN
    user, created = User.objects.get_or_create(username=ADMIN_USERNAME, defaults={'email': ADMIN_EMAIL, 'is_staff': True, 'is_superuser': True})

    # 2. ĐẶT MẬT KHẨU
    if created or not user.has_usable_password():
        user.set_password(NEW_PASSWORD)
        user.save()
        print(f"Password for {ADMIN_USERNAME} set/reset successfully!")
    else:
        # Luôn đặt lại mật khẩu để đảm bảo
        user.set_password(NEW_PASSWORD)
        user.save()
        print(f"Password for {ADMIN_USERNAME} reset successful.")

except Exception as e:
    print(f"FATAL ERROR during admin creation: {e}")