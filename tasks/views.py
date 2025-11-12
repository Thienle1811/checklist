from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponseForbidden
from .forms import TaskForm, TaskEditForm 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User 
from django.contrib import messages 
from .forms import CustomUserCreationForm, CustomUserChangeForm, AdminPasswordChangeForm 
from django.contrib.auth import update_session_auth_hash # Cần cho đổi mật khẩu

# Hàm kiểm tra user có phải là admin không (is_staff=True)
def is_admin(user):
    return user.is_staff

# **********************************************
# CÁC CHỨC NĂNG CHÍNH
# **********************************************

@login_required 
def dashboard(request):
    task_list = Task.objects.order_by('-created_at')
    
    paginator = Paginator(task_list, 10) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    
    # Không cần dùng assigned_name từ cookie nữa vì đã dùng user.username
    assigned_name = request.COOKIES.get('assignee_name') 
    
    context = {
        'page_obj': page_obj,
        'assigned_name': assigned_name # Giữ lại nếu bạn muốn dùng nó ở đâu đó khác
    }
    return render(request, 'tasks/dashboard.html', context)


# Cập nhật logic: Cho phép user đang đăng nhập nhận task nếu task chưa được gán
@login_required 
def enter_name(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Nếu task đã có người nhận (assigned_name), không cho phép nhận lại
    if task.assigned_name:
        messages.warning(request, f"Công việc '{task.task_name}' đã được gán/nhận bởi {task.assigned_name}.")
        return redirect('dashboard') 

    if request.method == 'POST':
        # Người nhận là username của user đang đăng nhập
        name = request.user.username
        
        if name:
            task.assigned_name = name
            task.is_received = True
            task.received_at = timezone.now()
            task.save()
            
            # Ghi nhớ tên vào cookie (tùy chọn)
            response = redirect('dashboard')
            response.set_cookie('assignee_name', name, max_age=2592000) 
            messages.success(request, f"Bạn đã nhận công việc '{task.task_name}'.")
            return response
        
    return redirect('dashboard')


# Cập nhật logic: Chỉ người được giao task mới được hoàn thành
@login_required 
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # KIỂM TRA QUYỀN: Nếu user không phải Admin VÀ không phải người được giao
    if not request.user.is_staff and task.assigned_name != request.user.username:
        messages.error(request, "Bạn không có quyền hoàn thành công việc này.")
        return redirect('dashboard') 
        
    if not task.assigned_name:
        messages.error(request, "Công việc chưa được gán hoặc nhận.")
        return redirect('dashboard')
    
    if not task.is_completed:
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
        messages.success(request, f"Đã hoàn thành công việc '{task.task_name}'.")
        
    return redirect('dashboard') 


# *************** CÁC CHỨC NĂNG ADMIN (QUẢN LÝ TASK) ***************

# Cập nhật logic: Xử lý việc gán task ban đầu
@login_required 
@user_passes_test(is_admin) 
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) 

            # Xử lý gán task
            assignee = form.cleaned_data.get('assignee')
            if assignee:
                task.assigned_name = assignee.username # Lưu username của người được gán
                task.is_received = True 
                task.received_at = timezone.now()
            elif task.assigned_name:
                 # Nếu người dùng bỏ chọn assignee, đặt lại trạng thái chưa nhận
                 task.assigned_name = None
                 task.is_received = False
                 task.received_at = None

            task.save()
            messages.success(request, "Tạo công việc thành công.")
            return redirect('dashboard') 
    else:
        form = TaskForm() 

    context = {'form': form}
    return render(request, 'tasks/task_form.html', context)


@login_required 
@user_passes_test(is_admin) 
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            
            # Xử lý khi Admin thay đổi người được gán trong Form Edit
            assignee = form.cleaned_data.get('assignee')
            
            if assignee:
                # Nếu Admin chọn người gán, cập nhật task đã nhận
                task.assigned_name = assignee.username
                if not task.is_received: # Chỉ cập nhật ngày nhận nếu chưa nhận
                    task.is_received = True
                    task.received_at = timezone.now()
            else:
                # Nếu Admin chọn '--- (Chưa nhận)', đặt lại
                task.assigned_name = None
                task.is_received = False
                task.received_at = None
                
            task.save()
            messages.success(request, f"Sửa công việc '{task.task_name}' thành công.")
            return redirect('dashboard')
    else:
        # Nếu task đã có người nhận, đặt giá trị ban đầu cho Form Edit
        initial_assignee = None
        if task.assigned_name:
            try:
                # Tìm user object từ assigned_name (username)
                initial_assignee = User.objects.get(username=task.assigned_name)
            except User.DoesNotExist:
                pass # Bỏ qua nếu user đã bị xóa
                
        form = TaskEditForm(instance=task, initial={'assignee': initial_assignee})


    context = {'form': form, 'task': task}
    return render(request, 'tasks/task_edit_form.html', context)


@login_required 
@user_passes_test(is_admin) 
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task_name = task.task_name
        task.delete()
        messages.success(request, f"Xóa công việc '{task_name}' thành công.")
        return redirect('dashboard')
        
    return redirect('dashboard')

# *************** CÁC CHỨC NĂNG QUẢN LÝ USER (GIỮ NGUYÊN) ***************

@login_required
@user_passes_test(is_admin) 
def manage_users(request):
    user_list = User.objects.exclude(id=request.user.id).order_by('username')
    context = {'user_list': user_list}
    return render(request, 'tasks/manage_users.html', context)

@login_required
@user_passes_test(is_admin) 
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tạo tài khoản mới thành công!")
            return redirect('manage-users')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'tasks/user_form.html', context)

@login_required
@user_passes_test(is_admin) 
def user_edit(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if user_to_edit.is_superuser: 
         messages.error(request, "Không được sửa đổi quyền Siêu Admin.")
         return redirect('manage-users')

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f"Sửa thông tin tài khoản '{user_to_edit.username}' thành công.")
            return redirect('manage-users')
    else:
        form = CustomUserChangeForm(instance=user_to_edit)
    
    context = {'form': form, 'user_to_edit': user_to_edit, 'action': 'Sửa'}
    return render(request, 'tasks/user_form.html', context)

@login_required
@user_passes_test(is_admin) 
def user_delete(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    
    if user_to_delete == request.user or user_to_delete.is_superuser:
        messages.error(request, "Không được xóa chính tài khoản của bạn hoặc Siêu Admin.")
        return redirect('manage-users')
        
    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"Xóa tài khoản '{username}' thành công.")
    
    return redirect('manage-users')
    
@login_required
@user_passes_test(is_admin) 
def admin_password_change(request):
    if request.method == 'POST':
        form = AdminPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            
            messages.success(request, 'Đổi mật khẩu thành công!')
            return redirect('dashboard')
    else:
        form = AdminPasswordChangeForm(request.user)
        
    context = {'form': form}
    return render(request, 'tasks/admin_password_change.html', context)