from django.db import models
# XÓA: from django.contrib.auth.models import User 

class Task(models.Model):
    # TRƯỜNG MỚI THAY THẾ User (Lưu tên người thực hiện)
    assigned_name = models.CharField(max_length=150, blank=True, null=True)
    
    task_name = models.CharField(max_length=255)
    sender_unit = models.CharField(max_length=255)
    due_date = models.DateTimeField() # Thời gian trả
    
    is_received = models.BooleanField(default=False)
    received_at = models.DateTimeField(null=True, blank=True) 
    
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name