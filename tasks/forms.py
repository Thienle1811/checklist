from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # Chỉ còn 3 trường này
        fields = [
            'task_name',
            'sender_unit',
            'due_date',
        ]
        
        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }
        
        # Đã xóa 'assignee' khỏi đây
        labels = {
            'task_name': 'Tên công việc',
            'sender_unit': 'Đơn vị gửi',
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