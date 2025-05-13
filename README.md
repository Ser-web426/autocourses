# autocourses

Платформа для поиска автокурсов.

## Функционал

- Регистрация, авторизация
- Создание, изменение, скрытие и удаление курсов
- Запись на курс
- Админ панель

## Требования 

- Python 3.13
- PostgreSQL

## Установка 

1. Клонирование репозитория
```bash
https://github.com/Ser-web426/autocourses.git
```
```bash
cd autocourses
```
2. Создание виртуального окружения
```bash
python -m venv .venv
```
```bash
.venv\Scripts\activate # On Linux: source venv/bin/activate 
```
3. Установка зависимостей
```bash
pip install -r requirements.txt 
```
4. Создание базы данных
Создаём базу данных с именем
```bash
autocourses_db
```
5. Создание миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Создание суперюзера
```bash
python manage.py createsuperuser
```
7. Запуск локального сервера
```bash
python manage.py runserver
```
8. Открыть в браузере [http://127.0.0.1:8000](http://127.0.0.1:8000)
