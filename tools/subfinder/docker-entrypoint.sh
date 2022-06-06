#!/bin/sh

chmod +x /app/tool/subfinder
celery -A subfinder worker -l info -c 1 -Q subfinder -n subfinder_$RANDOM --logfile=/app/logs/subfinder_celery.log >/dev/null 

