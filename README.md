# PhysLab

Тренажёр задач по физике — учебный проект на Django.

Позволяет выбирать раздел физики, решать задачи и видеть статистику ответов.

## Возможности

- Каталог задач по разделам физики (механика, оптика и др.)
- Три уровня сложности задач
- Проверка ответа с подсчётом статистики
- Страница статистики: общий процент и разбивка по темам
- Форма обратной связи
- Админ-панель для управления контентом

## Технологии

- Python 3.12
- Django 4.2
- SQLite
- Bootstrap 5
- Docker

## Структура проекта

```
physlab/
├── physlab/           # настройки Django-проекта
├── problems/          # основное приложение
│   ├── models.py      # Topic, Problem, Attempt, Feedback
│   ├── views.py       # 6 view-функций
│   ├── forms.py       # AnswerForm, FeedbackForm
│   ├── admin.py       # конфигурация админки
│   ├── urls.py        # маршруты приложения
│   └── tests.py       # 19 тестов
├── templates/         # HTML-шаблоны (Bootstrap 5)
├── Dockerfile
├── docker-compose.yml
└── Makefile
```

## Как запустить

### Локально

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

### Docker

```bash
make dev
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

Админ-панель: http://127.0.0.1:8000/admin/

## Makefile-команды

| Команда            | Описание                        |
|--------------------|----------------------------------|
| `make run`         | Запуск dev-сервера               |
| `make migrate`     | Применить миграции               |
| `make test`        | Запуск тестов                    |
| `make lint`        | Проверка кода (pylint)           |
| `make dev`         | Запуск через Docker              |
| `make superuser`   | Создать суперпользователя        |

## Автор

Дмитрий Глобин — [GitHub](https://github.com/DimaGlobin)
