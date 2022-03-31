#!/bin/sh

echo "Printing logs from db_manager in development" 
echo "Common log"
docker-compose -f docker-compose.yml --env-file .env.dev run db_manager cat "logs/logs.txt" 
echo "Interactions log"
docker-compose -f docker-compose.yml --env-file .env.dev run db_manager cat "logs/interactions_log.txt" 

