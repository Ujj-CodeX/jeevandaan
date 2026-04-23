python manage.py collectstatic --noinput --clear
gunicorn config.wsgi --timeout 120 --workers 2