# py-postgres-docker-learn
Learning project for python, docker, postgresql, logging
### development: docker
To deploy - from the root folder:
```Linux Kernel Module
docker-compose -f docker-compose.yml --env-file .env.dev up -d --build
```
All DB data will be reset with initial values, logs folder will be cleaned up
Log files available in ./logs folder.
To switch containers off:
```Linux Kernel Module
docker-compose -f docker-compose.yml --env-file .env.dev down -v
```
To do something with db:
```Linux Kernel Module
docker-compose -f docker-compose.yml --env-file .env.dev run db_manager python manage.py function_with_parameters
```
where "function_with_parameters" can be:
- create_db: clean DB and rebuild all the tables
- seed_db: fill DB with initial values
- add_hero name side_id birthday strength: add hero to DB, birthday and strength are both optional
- del_hero name: delete hero from DB, mottos are deleted too, all the interactions persist, but hero_id changes to null
- add_motto name txt: add motto for hero
- add_story name txt: add story for hero
- add_interaction: add interaction - heroes, mottos and winner are chosen randomly
### production: docker
```Linux Kernel Module
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```
To switch containers off:
```Linux Kernel Module
docker-compose -f docker-compose.prod.yml --env-file .env.prod down -v
```
To do something with db:
```Linux Kernel Module
docker-compose -f docker-compose.prod.yml --env-file .env.prod run db_manager python manage.py function_with_parameters
```
where "function_with_parameters" can be:
- create_db: clean DB and rebuild all the tables
- seed_db: fill DB with initial values
- add_hero name side_id birthday strength: add hero to DB, birthday and strength are both optional
- del_hero name: delete hero from DB, mottos are deleted too, all the interactions persist, but hero_id changes to null
- add_motto name txt: add motto for hero
- add_story name txt: add story for hero
- add_interaction: add interaction - heroes, mottos and winner are chosen randomly

