from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponseForbidden
from .forms import TaskForm, TaskEditForm
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    # Lấy tất cả công việc, sắp xếp cái mới nhất lên đầu
    task_list = Task.objects.order_by('-created_at')
    
    # Thiết lập phân trang: 10 công việc mỗi trang
    paginator = Paginator(task_list, 10) # 10 item/trang
    page_number = request.GET.get('page') # Lấy số trang từ URL (ví dụ: ?page=2)
    page_obj = paginator.get_page(page_number) # Lấy đối tượng trang
    
    # Gửi 'page_obj' (chứa 10 task) ra template
    context = {
        'page_obj': page_obj 
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def task_receive(request, task_id):
    # Lấy task, nếu không tìm thấy thì báo lỗi 404
    task = get_object_or_404(Task, id=task_id)
    
    # --- LOGIC MỚI (TỰ NHẬN VIỆC) - ĐÃ CẬP NHẬT Ở BƯỚC 30 ---
    # Chỉ gán việc nếu task đó CHƯA có người nhận
    if task.assignee is None:
        task.assignee = request.user  # Gán task cho người đang đăng nhập
        task.is_received = True
        task.received_at = timezone.now()
        task.save()
        
    return redirect('dashboard') # Quay lại trang dashboard

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # KIỂM TRA QUYỀN: Chỉ người được giao (assignee) mới được tick hoàn thành
    if request.user != task.assignee:
        # Nếu không đúng, trả về lỗi "Cấm"
        return HttpResponseForbidden("Bạn không có quyền hoàn thành công việc này.")
    
    # Đánh dấu là đã hoàn thành và ghi lại thời gian
    if not task.is_completed:
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
        
    return redirect('dashboard') # Quay lại trang dashboard

@login_required
def create_task(request):
    # Kiểm tra nếu không phải Admin, cấm truy cập
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save() # Lưu task mới vào CSDL
            return redirect('dashboard') # Quay lại dashboard
    else:
        form = TaskForm() # Tạo form rỗng

    # Gửi 'form' ra template
    context = {
        'form': form
    }
    return render(request, 'tasks/task_form.html', context)

@login_required
def manage_users(request):
    # Kiểm tra nếu không phải Admin, cấm truy cập
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")

    # Lấy tất cả user, ngoại trừ superuser (admin)
    user_list = User.objects.filter(is_superuser=False).order_by('username')

    context = {
        'user_list': user_list
    }
    return render(request, 'tasks/manage_users.html', context)

# ... (các view cũ) ...

@login_required
def task_edit(request, task_id):
    # Kiểm tra nếu không phải Admin, cấm truy cập
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        # Gửi dữ liệu POST vào form để cập nhật task
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # Tạo form với dữ liệu hiện tại của task
        form = TaskEditForm(instance=task)

    context = {
        'form': form,
        'task': task
    }
    # Chúng ta sẽ dùng chung template 'task_form.html'
    # nhưng sẽ tùy chỉnh nó một chút ở bước sau
    return render(request, 'tasks/task_edit_form.html', context)

@login_required
def task_delete(request, task_id):
    # Kiểm tra nếu không phải Admin, cấm truy cập
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")

    task = get_object_or_404(Task, id=task_id)

    # Chỉ xóa nếu request là POST (để an toàn)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')

    # Nếu là GET, chúng ta có thể hiển thị trang xác nhận (nhưng để đơn giản, 
    # chúng ta sẽ làm nút xóa bằng POST từ dashboard)
    return redirect('dashboard')