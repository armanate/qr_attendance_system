from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'student_string_id']
        labels = {
            'student_name': 'نام دانش‌آموز',
            'student_string_id': 'شماره دانش‌آموزی'
        }
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_string_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'student_name': 'Student Name',
            'student_string_id': 'Student ID',
        }