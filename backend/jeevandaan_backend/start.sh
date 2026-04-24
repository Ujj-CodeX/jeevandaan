python manage.py collectstatic --noinput --clear
gunicorn config.wsgi:application --workers 2 --timeout 120 --preload