# text-remove-web (Django)

Small Django app that removes a marked part from submitted text.

## Run

```
cd text-remove-web
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install django
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000

## Admin words

Words to remove are stored in the database and edited via `/admin`.

```
python manage.py createsuperuser
```

Defaults live in `textremove_web/settings.py`:
- `DEFAULT_REMOVE_WORDS`
