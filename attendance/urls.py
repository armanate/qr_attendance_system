from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:student_id>/qr/', views.generate_qr, name='generate_qr'),
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('scan/', views.scan_qr, name='scan_qr'),
    path('process-qr/', views.process_qr_data, name='process_qr_data'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('attendance/reset/', views.reset_attendance, name='reset_attendance'),
]