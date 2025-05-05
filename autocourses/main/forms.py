from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Course

class BaseUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'})
    )
    phone_number = forms.CharField(
        label='Номер телефона',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'})
    )
    full_name = forms.CharField(
        label='Полное имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите полное имя'})
    )
    birth_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    driving_experience = forms.IntegerField(
        label='Стаж вождения (годы)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите стаж вождения'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'full_name', 'birth_date', 'driving_experience', 'password1', 'password2')


class StudentRegistrationForm(BaseUserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        if commit:
            user.save()
        return user


class InstructorRegistrationForm(BaseUserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.INSTRUCTOR
        if commit:
            user.save()
        return user

class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'start_date', 'end_date', 'price', 'is_hidden', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_hidden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Название курса',
            'description': 'Описание',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'price': 'Стоимость (руб.)',
            'is_hidden': 'Скрыть курс',
            'image': 'Изображение',
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )


class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'start_date', 'end_date', 'price', 'is_hidden', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_hidden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Название курса',
            'description': 'Описание',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'price': 'Стоимость (руб.)',
            'is_hidden': 'Скрыть курс',
            'image': 'Изображение',
        }

    class CourseEditForm(forms.ModelForm):
        class Meta:
            model = Course
            fields = ('title', 'description', 'start_date', 'end_date', 'price', 'is_hidden', 'image')
            widgets = {
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'price': forms.NumberInput(attrs={'class': 'form-control'}),
                'is_hidden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            }
            labels = {
                'title': 'Название курса',
                'description': 'Описание',
                'start_date': 'Дата начала',
                'end_date': 'Дата окончания',
                'price': 'Стоимость (руб.)',
                'is_hidden': 'Скрыть курс',
                'image': 'Изображение',
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            print("Instance in form:", self.instance)
            # Удаляем ручную установку initial, так как Django сделает это автоматически