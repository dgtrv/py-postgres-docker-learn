#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"


if [ "$STAGE" = "dev" ]
then
    echo "Cleaning up logs folder"
    rm -rf ./logs/*
    echo "Creating the database tables..."
    python manage.py create_db
    echo "Filling tables with ini data..."
    python manage.py seed_db
    echo "Tables created and filled."
fi

exec "$@"
