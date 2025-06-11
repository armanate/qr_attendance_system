from django.db import models
from django.utils import timezone

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    student_string_id = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.student_name} ({self.student_string_id})"
    
    class Meta:
        ordering = ['student_name']

class PresentStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.student.student_name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        unique_together = ['student']
        ordering = ['-timestamp'] 
