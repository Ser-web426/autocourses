from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Студент'
        INSTRUCTOR = 'instructor', 'Инструктор'

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=False, blank=True, default='2000-01-01')
    driving_experience = models.PositiveIntegerField(help_text='Водительский стаж в годах', default=0)

    def __str__(self):
        return self.full_name


class Course(models.Model):
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    authors = models.ManyToManyField(User, related_name='authored_courses')
    is_hidden = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class CourseEnrollment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'На подтверждении'
        CONFIRMED = 'confirmed', 'Подтверждено'

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.full_name} -> {self.course.title} ({self.get_status_display()})"
