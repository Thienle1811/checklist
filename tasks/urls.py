from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    # LOGIN / LOGOUT
    path('login/', LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    
    # CHỨC NĂNG CHÍNH
    path('', views.dashboard, name='dashboard'), 
    path('enter/<int:task_id>/', views.enter_name, name='enter-name'),
    path('complete/<int:task_id>/', views.task_complete, name='task-complete'),
    
    # QUẢN LÝ TASK (ADMIN ONLY)
    path('create/', views.create_task, name='task-create'),
    path('edit/<int:task_id>/', views.task_edit, name='task-edit'),
    path('delete/<int:task_id>/', views.task_delete, name='task-delete'),
    
    # ===============================================
    # THÊM QUẢN LÝ USER VÀ ĐỔI MẬT KHẨU ADMIN MỚI
    # ===============================================
    path('users/', views.manage_users, name='manage-users'),
    path('users/add/', views.user_create, name='user-create'),
    path('users/edit/<int:user_id>/', views.user_edit, name='user-edit'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user-delete'),
    path('admin/password/change/', views.admin_password_change, name='admin-password-change'),
]