from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponseForbidden
from .forms import TaskForm, TaskEditForm 


# **********************************************
# LƯU Ý: ADMIN VẪN CÓ THỂ ĐĂNG NHẬP QUA /admin/
# **********************************************


def dashboard(request):
    task_list = Task.objects.order_by('-created_at')
    
    paginator = Paginator(task_list, 10) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    
    # 1. ĐỌC TÊN TỪ COOKIE (TÍNH NĂNG GHI NHỚ)
    assigned_name = request.COOKIES.get('assignee_name') 
    
    context = {
        'page_obj': page_obj,
        'assigned_name': assigned_name # Gửi tên đã ghi nhớ ra template
    }
    return render(request, 'tasks/dashboard.html', context)


def enter_name(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # 1. Nếu công việc đã có người nhận, không cho phép nhận lại
    if task.assigned_name:
        return redirect('dashboard') 

    if request.method == 'POST':
        # Lấy tên từ Form POST
        name = request.POST.get('assignee_name')
        
        if name:
            task.assigned_name = name
            task.is_received = True
            task.received_at = timezone.now()
            task.save()
            
            # 2. GHI TÊN VÀO COOKIE VÀ TRẢ VỀ PHẢN HỒI (TÍNH NĂNG GHI NHỚ)
            response = redirect('dashboard')
            # Ghi nhớ tên trong 30 ngày (2592000 giây)
            response.set_cookie('assignee_name', name, max_age=2592000) 
            return response
        
    return redirect('dashboard')


def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # KIỂM TRA QUYỀN: Chỉ cho phép hoàn thành nếu ĐÃ có người nhận
    if not task.assigned_name:
        return HttpResponseForbidden("Công việc chưa được nhận.")
    
    if not task.is_completed:
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
        
    return redirect('dashboard') 


# *************** CÁC CHỨC NĂNG ADMIN (GIỮ LẠI) ***************

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('dashboard') 
    else:
        form = TaskForm() 

    context = {'form': form}
    return render(request, 'tasks/task_form.html', context)


def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskEditForm(instance=task)

    context = {'form': form, 'task': task}
    return render(request, 'tasks/task_edit_form.html', context)

def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
        
    return redirect('dashboard')