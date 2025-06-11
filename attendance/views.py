import os
import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
from .models import Student, PresentStudent
from .forms import StudentForm

def home(request):
    return render(request, 'attendance/home.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'دانش‌آموز با موفقیت اضافه شد!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'attendance/add_student.html', {'form': form})

def generate_qr(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Create QR code directory if it doesn't exist
    qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(student.student_string_id)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code image
    img_path = os.path.join(qr_dir, f"{student.student_string_id}.png")
    img.save(img_path)
    
    # Get relative path for template
    relative_path = f"media/qrcodes/{student.student_string_id}.png"
    
    return render(request, 'attendance/qr_code.html', {
        'student': student,
        'qr_code_path': relative_path
    })

def scan_qr(request):
    return render(request, 'attendance/scan_qr.html')

@csrf_exempt
def process_qr_data(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        try:
            student = Student.objects.get(student_string_id=data)
            # Check if student is already marked present today
            today = timezone.now().date()
            if PresentStudent.objects.filter(student=student, timestamp__date=today).exists():
                return JsonResponse({
                    'success': False,
                    'message': f'دانش‌آموز {student.student_name} قبلاً حاضر شده است!'
                })
            else:
                PresentStudent.objects.create(student=student)
                return JsonResponse({
                    'success': True,
                    'message': f'دانش‌آموز {student.student_name} با موفقیت حاضر شد!'
                })
        except Student.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': f'دانش‌آموز با شماره {data} یافت نشد!'
            })
    return JsonResponse({
        'success': False,
        'message': 'درخواست نامعتبر!'
    })

def attendance_view(request):
    # Get present students
    present_students = PresentStudent.objects.select_related('student').all()
    
    # Get all student IDs that are present
    present_student_ids = present_students.values_list('student_id', flat=True)
    
    # Get absent students
    absent_students = Student.objects.exclude(id__in=present_student_ids)
    
    # Convert current date to Persian (Jalali) date
    import jdatetime
    jdatetime.set_locale('fa_IR')
    current_date = jdatetime.datetime.now().strftime('%Y/%m/%d')
    
    return render(request, 'attendance/attendance.html', {
        'present_students': present_students,
        'absent_students': absent_students,
        'current_date': current_date
    })

def reset_attendance(request):
    if request.method == 'POST':
        today = timezone.now().date()
        PresentStudent.objects.filter(timestamp__date=today).delete()
        return JsonResponse({
            'success': True,
            'message': 'لیست حضور و غیاب با موفقیت بازنشانی شد!'
        })
    return JsonResponse({
        'success': False,
        'message': 'درخواست نامعتبر!'
    })

def delete_student(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        student_name = student.student_name
        student.delete()
        messages.success(request, f'دانش‌آموز {student_name} با موفقیت حذف شد!')
    return redirect('student_list')
