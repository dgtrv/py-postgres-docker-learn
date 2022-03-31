#!/bin/sh

echo "Running shell in db_manager on production"
exec docker-compose -f docker-compose.prod.yml --env-file .env.prod run db_manager sh "$@" 

