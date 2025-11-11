from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # XÓA: path('receive/<int:task_id>/', views.task_receive, name='task-receive'),
    # THÊM:
    path('enter/<int:task_id>/', views.enter_name, name='enter-name'),
    
    path('complete/<int:task_id>/', views.task_complete, name='task-complete'),
    path('create/', views.create_task, name='task-create'),
    # XÓA: path('users/', views.manage_users, name='manage-users'), # Không cần quản lý user khi bỏ đăng nhập
    path('edit/<int:task_id>/', views.task_edit, name='task-edit'),
    path('delete/<int:task_id>/', views.task_delete, name='task-delete'),
]