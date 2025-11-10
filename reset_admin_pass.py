import os
import django

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

# Mật khẩu mới
NEW_PASSWORD = 'MyFinalSecurePass2025!' # <--- ĐẶT MẬT KHẨU CỦA BẠN VÀO ĐÂY
ADMIN_USERNAME = 'admin'

try:
    User = get_user_model()
    user = User.objects.get(username=ADMIN_USERNAME)
    user.set_password(NEW_PASSWORD)
    user.save()
    print(f"Password for {ADMIN_USERNAME} reset successfully!")
except User.DoesNotExist:
    print(f"User {ADMIN_USERNAME} does not exist. Cannot reset password.")
except Exception as e:
    print(f"An error occurred: {e}")