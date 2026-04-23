python manage.py collectstatic --noinput
gunicorn config.wsgi --timeout 120 --workers 2