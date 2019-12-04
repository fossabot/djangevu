#!/bin/bash
python manage.py collectstatic --noinput
uwsgi --ini=uwsgi.ini --uid $UID --gid $GID
