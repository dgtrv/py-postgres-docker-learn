#!/bin/sh

echo "Shutting down production..."
exec docker-compose -f docker-compose.prod.yml --env-file .env.prod down 

