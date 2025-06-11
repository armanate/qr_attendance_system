from django.contrib import admin
from .models import Student, PresentStudent

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_name', 'student_string_id')
    search_fields = ('student_name', 'student_string_id')
    ordering = ('student_name',)

@admin.register(PresentStudent)
class PresentStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_student_name', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('student__student_name',)
    ordering = ('-timestamp',)
    
    def get_student_name(self, obj):
        return obj.student.student_name
    
    get_student_name.short_description = 'Student Name'
