python manage.py collectstatic --noinput --clear
gunicorn config.wsgi --timeout 120 --workers 2 --worker-class sync --keepalive  5 --preload_app  True --max_requests  500 --max_requests_jitter  50