#!/bin/sh

echo "Running commands \"$@\" on development"
exec docker-compose -f docker-compose.yml --env-file .env.dev run db_manager python manage.py "$@" 

