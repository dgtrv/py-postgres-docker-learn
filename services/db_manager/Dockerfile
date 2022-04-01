# pull base image
FROM python:3.10.2-alpine

# variable from docker-compose
ARG DB_MANAGER_APP_PATH

# set work directory
WORKDIR ${DB_MANAGER_APP_PATH}

# install netcat for checking db availability on start
RUN apk update && apk add netcat-openbsd

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ${DB_MANAGER_APP_PATH}requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . ${DB_MANAGER_APP_PATH}

# make intrypoint executable
RUN chmod +x ${DB_MANAGER_APP_PATH}entrypoint.sh

# run entrypoint.prod.sh
CMD ${DB_MANAGER_APP_PATH}entrypoint.sh
