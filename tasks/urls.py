from django.urls import path
from . import views # Import các views từ thư mục hiện tại

urlpatterns = [
    # Trang chủ sẽ trỏ đến view 'dashboard'
    path('', views.dashboard, name='dashboard'),
    path('receive/<int:task_id>/', views.task_receive, name='task-receive'),
    path('complete/<int:task_id>/', views.task_complete, name='task-complete'),
    path('create/', views.create_task, name='task-create'),
    path('users/', views.manage_users, name='manage-users'),
    path('edit/<int:task_id>/', views.task_edit, name='task-edit'),
    path('delete/<int:task_id>/', views.task_delete, name='task-delete'),
]