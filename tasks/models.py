from django.db import models
from django.contrib.auth.models import User 

class Task(models.Model):
    # TẤT CẢ các dòng dưới đây phải được thụt vào 4 dấu cách
    
    # Dòng này đã được sửa với null=True
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    
    task_name = models.CharField(max_length=255)
    sender_unit = models.CharField(max_length=255)
    due_date = models.DateTimeField() # Thời gian trả
    
    # Các trường theo dõi trạng thái
    is_received = models.BooleanField(default=False)
    received_at = models.DateTimeField(null=True, blank=True) # Thời gian nhận
    
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True) # Thời gian hoàn thành
    
    # Tự động thêm ngày tạo khi 1 task được tạo ra
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name