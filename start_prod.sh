#!/bin/sh

echo "Starting production..."
exec docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
