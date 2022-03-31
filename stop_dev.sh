#!/bin/sh

echo "Shutting down development..."
exec docker-compose -f docker-compose.yml --env-file .env down -v 

