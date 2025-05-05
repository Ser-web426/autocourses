from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Course, CourseEnrollment, User
from django.contrib.auth.views import LoginView
from .forms import StudentRegistrationForm, InstructorRegistrationForm, CourseCreationForm, CustomAuthenticationForm, CourseEditForm

class CustomLoginView(LoginView):
    template_name = "main/login.html"
    authentication_form = CustomAuthenticationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:profile')
        return super().get(request, *args, **kwargs)

def register_student(request):
    if(request.user.is_authenticated):
        return redirect('main:profile')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация студента прошла успешно!')
            return redirect('/main/profile')
    else:
        form = StudentRegistrationForm()
    return render(request, 'main/register.html', {'form': form, 'user_type': 'студента'})

def register_instructor(request):
    if(request.user.is_authenticated):
        return redirect('main:profile')
    if request.method == 'POST':
        form = InstructorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация инструктора прошла успешно!')
            return redirect('/main/profile')
    else:
        form = InstructorRegistrationForm()
    return render(request, 'main/register.html', {'form': form, 'user_type': 'инструктора'})

def register(request):
    if(request.user.is_authenticated):
        return redirect('main:profile')
    return render(request, 'main/who_iam.html')

@login_required
def profile(request):
    enrollments = CourseEnrollment.objects.filter(student=request.user) if request.user.role == User.Role.STUDENT else CourseEnrollment.objects.filter(course__authors=request.user, status='pending')
    return render(request, 'main/profile.html', {'enrollments': enrollments})

def course_list(request):
    courses = Course.objects.filter(is_hidden=False)
    return render(request, 'main/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment = None
    pending_enrollments = []
    confirmed_enrollments = []

    if request.user.is_authenticated:
        if request.user.role == User.Role.STUDENT:
            enrollment = CourseEnrollment.objects.filter(student=request.user, course=course).first()

        if request.user in course.authors.all():
            pending_enrollments = CourseEnrollment.objects.filter(course=course, status='pending')
            confirmed_enrollments = CourseEnrollment.objects.filter(course=course, status='confirmed')

    return render(request, 'main/course_detail.html', {
        'course': course,
        'enrollment': enrollment,
        'pending_enrollments': pending_enrollments,
        'confirmed_enrollments': confirmed_enrollments,
    })

# Представление записи на курс
@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.role != User.Role.STUDENT:
        messages.error(request, 'Только студенты могут записываться на курсы.')
        return redirect(f'/main/courses/{course.id}')
    enrollment, created = CourseEnrollment.objects.get_or_create(student=request.user, course=course, defaults={'status': 'pending'})
    if created:
        messages.success(request, 'Заявка на курс отправлена.')
    else:
        messages.info(request, 'Вы уже подали заявку или записаны на этот курс.')
    return redirect(f'/main/courses/{course.id}')

@login_required
def unenroll_from_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.role != User.Role.STUDENT:
        messages.error(request, 'Только студенты могут отписываться от курсов.')
        return redirect(f'/main/courses/{course.id}')
    enrollment = CourseEnrollment.objects.filter(student=request.user, course=course).first()
    if enrollment:
        enrollment.delete()
        messages.success(request, 'Вы отписались от курса.')
    else:
        messages.error(request, 'Вы не записаны на этот курс.')
    return redirect(f'/main/courses/{course.id}')

@login_required
def confirm_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id)
    if request.user not in enrollment.course.authors.all():
        return HttpResponseForbidden('Только автор курса может подтверждать заявки.')
    if request.method == 'POST':
        enrollment.status = 'confirmed'
        enrollment.save()
        messages.success(request, 'Заявка студента подтверждена.')
    return redirect('main:course_detail', course_id=enrollment.course.id)


# Представление создания курса
@login_required
def create_course(request):
    if request.user.role != User.Role.INSTRUCTOR:
        return HttpResponseForbidden('Только инструкторы могут создавать курсы.')
    if request.method == 'POST':
        form = CourseCreationForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            course.authors.add(request.user)
            messages.success(request, 'Курс успешно создан!')
            return redirect(f'/main/courses/{course.id}')
    else:
        form = CourseCreationForm()
    return render(request, 'main/create_course.html', {'form': form})

@login_required
def hide_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user not in course.authors.all():
        messages.error(request, 'Только автор курса может скрывать или показывать курс.')
        return redirect('/main/profile')
    if request.method == 'POST':
        course.is_hidden = not course.is_hidden
        course.save()
        status = 'скрыт' if course.is_hidden else 'показан'
        messages.success(request, f'Курс "{course.title}" успешно {status}.')
    return redirect('/main/profile')

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user not in course.authors.all():
        messages.error(request, 'Только автор курса может удалять курс.')
        return redirect('/main/profile')
    if request.method == 'POST':
        course_title = course.title
        course.delete()
        messages.success(request, f'Курс "{course_title}" успешно удалён.')
    return redirect('/main/profile')


@login_required
def exclude_student(request, enrollment_id):
    enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id)

    if request.user not in enrollment.course.authors.all():
        messages.error(request, 'Только автор курса может исключить участников.')
        return redirect('main:course_detail', course_id=enrollment.course.id)

    enrollment.delete()
    messages.success(request, 'Студент был исключён из курса.')

    return redirect('main:course_detail', course_id=enrollment.course.id)

@login_required
def reject_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id)

    if request.user not in enrollment.course.authors.all():
        messages.error(request, 'Только автор курса может исключить участников.')
        return redirect('main:course_detail', course_id=enrollment.course.id)

    enrollment.delete()
    messages.success(request, 'Студент был исключён из курса.')

    return redirect('main:course_detail', course_id=enrollment.course.id)


def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user not in course.authors.all():
        messages.error(request, 'Только автор курса может исключить участников.')
        return redirect('main:profile')

    if request.method == 'POST':
        form = CourseEditForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('main:course_detail', course_id=course.id)
    else:
        form = CourseEditForm(instance=course)
    return render(request, 'main/edit_course.html', {'form': form, 'course': course})