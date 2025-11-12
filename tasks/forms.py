from django import forms
from .models import Task
from django.contrib.auth.models import User
# THÊM: Forms của Django để quản lý User và Password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm


class TaskForm(forms.ModelForm):
    # THÊM TRƯỜNG ASSIGNEE CHO FORM TẠO TASK
    assignee = forms.ModelChoiceField(
        queryset=User.objects.all(), # Cho phép gán cho mọi User (Admin & User thường)
        required=False, # Cho phép để trống (tức là chưa gán)
        label="Giao cho (Người nhận)",
        empty_label="--- (Chưa gán) ---" # Hiển thị lựa chọn rỗng
    )
    
    class Meta:
        model = Task
        # CẬP NHẬT: Thêm 'assignee' vào fields
        fields = [
            'task_name',
            'sender_unit',
            'assignee', 
            'due_date',
        ]
        
        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }
        
        labels = {
            'task_name': 'Tên công việc',
            'sender_unit': 'Đơn vị gửi',
            # 'assignee' đã được định nghĩa label ở trên
            'due_date': 'Thời gian trả',
        }

class TaskEditForm(forms.ModelForm):
    # Chúng ta dùng ModelChoiceField để cho phép Admin chọn '---' (trống)
    # để gán task về lại "Chưa nhận"
    assignee = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=False), # Chỉ cho phép gán cho user, không gán cho admin
        required=False, # Cho phép để trống (null)
        label="Giao cho (Người nhận)",
        empty_label="--- (Chưa nhận) ---" # Hiển thị lựa chọn rỗng
    )

    class Meta:
        model = Task
        # Lần này chúng ta đưa 'assignee' vào
        fields = [
            'task_name',
            'sender_unit',
            'assignee', 
            'due_date',
        ]

        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

        labels = {
            'task_name': 'Tên công việc',
            'sender_unit': 'Đơn vị gửi',
            'due_date': 'Thời gian trả',
        }
        
# ===============================================
# CÁC USER FORMS (GIỮ NGUYÊN)
# ===============================================

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff')
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Email',
            'first_name': 'Tên',
            'last_name': 'Họ',
            'is_staff': 'Là Admin (Cho phép quản lý Task)',
        }

class CustomUserChangeForm(UserChangeForm):
    # Loại bỏ trường password vì chúng ta dùng form đổi password riêng
    password = None 
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Email',
            'first_name': 'Tên',
            'last_name': 'Họ',
            'is_staff': 'Là Admin (Quản lý Task)',
            'is_active': 'Hoạt động',
        }
        
class AdminPasswordChangeForm(PasswordChangeForm):
    # Sử dụng form mặc định, chỉ cần kế thừa
    pass