python manage.py migrate
gunicorn kodo_project.wsgi -b 0.0.0.0:9000 --reload