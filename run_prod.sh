#!/bin/sh

echo "Running commands \"$@\" on production"
exec docker-compose -f docker-compose.prod.yml --env-file .env.prod run db_manager python manage.py "$@" 

