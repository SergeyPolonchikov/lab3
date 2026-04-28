# Lab 3 — Flask

Функциональность:

- `/counter` — счётчик посещений страницы на базе `session`.
- Аутентификация через `Flask-Login`:
  - логин: `user`
  - пароль: `qwerty`
  - чекбокс **«Запомнить меня»** сохраняет сессию после закрытия браузера (cookie remember).
- `/secret` — доступна только аутентифицированным пользователям; при попытке доступа происходит редирект на `/login` с сообщением и возвратом на запрошенную страницу после входа.

## Запуск локально

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Открыть: `http://127.0.0.1:5000`

## Деплой (пример: Render)

1. Загрузите репозиторий на GitHub.
2. На Render создайте **Web Service** из репозитория.
3. В настройках:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
   - Environment: `SECRET_KEY` (задайте случайную строку)

После деплоя Render выдаст URL приложения.

