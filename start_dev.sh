#!/bin/sh

echo "Starting development..."
exec docker-compose -f docker-compose.yml --env-file .env.dev up -d --build
