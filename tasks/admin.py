from django.contrib import admin
from .models import Task  # Import model Task của bạn

# Đăng ký model Task
admin.site.register(Task)