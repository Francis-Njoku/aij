release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn aij.wsgi
REMAP_SIGTERM=SIGQUIT