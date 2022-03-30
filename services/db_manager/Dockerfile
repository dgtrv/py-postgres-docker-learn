FROM python:3.10.2-alpine

WORKDIR ${DB_MANAGER_APP_PATH}

RUN apk update && apk add netcat-openbsd

RUN pip install --upgrade pip
COPY ./requirements.txt ${DB_MANAGER_APP_PATH}requirements.txt
RUN pip install -r requirements.txt

COPY . ${DB_MANAGER_APP_PATH}

RUN chmod +x ${DB_MANAGER_APP_PATH}entrypoint.sh

CMD ${DB_MANAGER_APP_PATH}entrypoint.sh
