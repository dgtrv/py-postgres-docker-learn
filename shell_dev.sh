#!/bin/sh

echo "Running shell in db_manager on development"
exec docker-compose -f docker-compose.yml --env-file .env.dev run db_manager sh "$@" 

