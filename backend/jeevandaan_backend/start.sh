python manage.py collectstatic --noinput
gunicorn config.wsgi:application --timeout 60