#!/bin/sh

echo "Printing logs from db_manager in production"
echo "Common log"
docker-compose -f docker-compose.prod.yml --env-file .env.prod run db_manager cat "logs/logs.txt" 
echo "Interactions log"
docker-compose -f docker-compose.prod.yml --env-file .env.prod run db_manager cat "logs/interactions_log.txt" 

