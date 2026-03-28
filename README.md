# PhysLab

Тренажёр задач по физике — учебный проект на Django.

Позволяет выбирать раздел физики, решать задачи и видеть статистику ответов.

## Технологии

- Python 3.9+
- Django 4.2
- SQLite
- Bootstrap 5

## Как запустить

```bash
# Клонировать репозиторий
git clone git@github.com:DimaGlobin/physlab.git
cd physlab

# Создать виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Создать суперпользователя (для админки)
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

Админ-панель: http://127.0.0.1:8000/admin/

## Автор

Дмитрий Глобин — [GitHub](https://github.com/DimaGlobin)
