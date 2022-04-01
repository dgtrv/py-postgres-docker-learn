# py-postgres-docker-learn
Learning project for python, docker, postgresql, logging
### development: docker
To deploy - from the root folder:
```Linux Kernel Module
./start_dev.sh
```
All DB data will be reset with initial values, logs folder will be cleaned up
Log files available in ./logs folder.
To switch containers off:
```Linux Kernel Module
./stop_dev.sh
```
To do something with db:
```Linux Kernel Module
./run_dev.sh function_with_parameters
```
where "function_with_parameters" can be:
- create_db: clean DB and rebuild all the tables
- seed_db: fill DB with initial values
- add_hero name side_id birthday strength: add hero to DB, birthday and strength are both optional
- del_hero name: delete hero from DB, mottos are deleted too, all the interactions persist, but hero_id changes to null
- add_motto name txt: add motto for hero
- add_story name txt: add story for hero
- add_interaction: add interaction - heroes, mottos and winner are chosen randomly

To view log files:
```Linux Kernel Module
./logs_dev.sh
```
To access db_manager container shell:
```Linux Kernel Module
./shell_dev.sh
```
### production: docker
To deploy - from the root folder:
```Linux Kernel Module
./start_prod.sh
```
To switch containers off (all the data in db and logs will persist):
```Linux Kernel Module
./stop_prod.sh
```
To do something with db:
```Linux Kernel Module
./run_prod.sh function_with_parameters
```
where "function_with_parameters" can be:
- create_db: clean DB and rebuild all the tables
- seed_db: fill DB with initial values
- add_hero name side_id birthday strength: add hero to DB, birthday and strength are both optional
- del_hero name: delete hero from DB, mottos are deleted too, all the interactions persist, but hero_id changes to null
- add_motto name txt: add motto for hero
- add_story name txt: add story for hero
- add_interaction: add interaction - heroes, mottos and winner are chosen randomly

To access db_manager container shell:
```Linux Kernel Module
./shell_prod.sh
```
To view log files:
```Linux Kernel Module
./logs_prod.sh
```

### DB tables description
(also in txt files in project root folder)

                                      Table "public.heroes"
  Column  |           Type           | Collation | Nullable |              Default               
----------|--------------------------|-----------|----------|------------------------------------
 id       | integer                  |           | not null | nextval('heroes_id_seq'::regclass)
 side_id  | integer                  |           | not null | 
 name     | character varying(30)    |           | not null | 
 birthday | timestamp with time zone |           |          | 
 strength | integer                  |           |          | 

Indexes:
-    "heroes_pkey" PRIMARY KEY, btree (id)

Foreign-key constraints:
-    "heroes_side_id_fkey" FOREIGN KEY (side_id) REFERENCES sides(id)

Referenced by:
-    TABLE "interactions" CONSTRAINT "interactions_hero_1_id_fkey" FOREIGN KEY (hero_1_id) REFERENCES heroes(id) ON DELETE SET NULL
-    TABLE "interactions" CONSTRAINT "interactions_hero_2_id_fkey" FOREIGN KEY (hero_2_id) REFERENCES heroes(id) ON DELETE SET NULL
-    TABLE "mottos" CONSTRAINT "mottos_hero_id_fkey" FOREIGN KEY (hero_id) REFERENCES heroes(id)
-    TABLE "stories" CONSTRAINT "stories_hero_id_fkey" FOREIGN KEY (hero_id) REFERENCES heroes(id)


                                   Table "public.sides"
 Column |         Type          | Collation | Nullable |              Default              
--------|-----------------------|-----------|----------|-----------------------------------
 id     | integer               |           | not null | nextval('sides_id_seq'::regclass)
 name   | character varying(30) |           | not null | 

Indexes:
-    "sides_pkey" PRIMARY KEY, btree (id)

Referenced by:
-    TABLE "heroes" CONSTRAINT "heroes_side_id_fkey" FOREIGN KEY (side_id) REFERENCES sides(id)


                                     Table "public.mottos"
  Column  |          Type          | Collation | Nullable |              Default               
----------|------------------------|-----------|----------|------------------------------------
 id       | integer                |           | not null | nextval('mottos_id_seq'::regclass)
 hero_id  | integer                |           |          | 
 motto_id | integer                |           |          | 
 motto    | character varying(500) |           | not null | 

Indexes:
-    "mottos_pkey" PRIMARY KEY, btree (id)

Foreign-key constraints:
-    "mottos_hero_id_fkey" FOREIGN KEY (hero_id) REFERENCES heroes(id)

Referenced by:
-    TABLE "interactions" CONSTRAINT "interactions_hero_1_motto_id_fkey" FOREIGN KEY (hero_1_motto_id) REFERENCES mottos(id) ON DELETE SET NULL
-    TABLE "interactions" CONSTRAINT "interactions_hero_2_motto_id_fkey" FOREIGN KEY (hero_2_motto_id) REFERENCES mottos(id) ON DELETE SET NULL


                                    Table "public.stories"
 Column  |          Type          | Collation | Nullable |               Default               
---------|------------------------|-----------|----------|-------------------------------------
 id      | integer                |           | not null | nextval('stories_id_seq'::regclass)
 hero_id | integer                |           | not null | 
 story   | character varying(500) |           | not null | 

Indexes:
-    "stories_pkey" PRIMARY KEY, btree (id)

Foreign-key constraints:
-    "stories_hero_id_fkey" FOREIGN KEY (hero_id) REFERENCES heroes(id)


                                 Table "public.interactions"
   Column        |  Type   | Collation | Nullable |                 Default                  
-----------------|---------|-----------|----------|------------------------------------------
 id              | integer |           | not null | nextval('interactions_id_seq'::regclass)
 hero_1_id       | integer |           |          | 
 hero_1_motto_id | integer |           |          | 
 hero_2_id       | integer |           |          | 
 hero_2_motto_id | integer |           |          | 
 winner          | integer |           |          | 

Indexes:
-    "interactions_pkey" PRIMARY KEY, btree (id)

Foreign-key constraints:
-    "interactions_hero_1_id_fkey" FOREIGN KEY (hero_1_id) REFERENCES heroes(id) ON DELETE SET NULL
-    "interactions_hero_1_motto_id_fkey" FOREIGN KEY (hero_1_motto_id) REFERENCES mottos(id) ON DELETE SET NULL
-    "interactions_hero_2_id_fkey" FOREIGN KEY (hero_2_id) REFERENCES heroes(id) ON DELETE SET NULL
-    "interactions_hero_2_motto_id_fkey" FOREIGN KEY (hero_2_motto_id) REFERENCES mottos(id) ON DELETE SET NULL

