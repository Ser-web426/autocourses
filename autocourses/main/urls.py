from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import CustomAuthenticationForm

app_name = "main"

urlpatterns = [
    path("courses/", views.course_list, name="course_list"),
    path("courses/<int:course_id>/", views.course_detail, name="course_detail"),
    path(
        "courses/<int:course_id>/enroll/",
        views.enroll_in_course,
        name="enroll_in_course",
    ),
    path(
        "courses/<int:course_id>/unenroll/",
        views.unenroll_from_course,
        name="unenroll_from_course",
    ),
    path("courses/<int:course_id>/hide/", views.hide_course, name="hide_course"),
    path(
        "courses/<int:course_id>/delete_course/",
        views.delete_course,
        name="delete_course",
    ),
    path(
        "enrollments/<int:enrollment_id>/confirm/",
        views.confirm_enrollment,
        name="confirm_enrollment",
    ),
    path("profile/", views.profile, name="profile"),
    path('register/student/', views.register_student, name='register_student'),
    path('register/instructor/', views.register_instructor, name='register_instructor'),
    path(
        "login/",
        views.CustomLoginView.as_view(
            template_name="main/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="login",
    ),
    path('register', views.register, name='register'),
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="/main/login"), name="logout"
    ),
    path('exclude_student/<int:enrollment_id>/', views.exclude_student, name='exclude_student'),
    path("courses/create/", views.create_course, name="create_course"),
    path('reject_enrollment/<int:enrollment_id>/', views.reject_enrollment, name='reject_enrollment'),
    path('course/edit/<int:course_id>/', views.edit_course, name='edit_course'),
]
