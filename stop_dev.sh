#!/bin/sh

echo "Shutting down development..."
exec docker-compose -f docker-compose.yml --env-file .env.dev down -v 

