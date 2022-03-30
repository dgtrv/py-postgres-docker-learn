FROM python:3.10.2-alpine

WORKDIR ${DB_MANAGER_APP_DIR}

RUN apk update && apk add netcat-openbsd

RUN pip install --upgrade pip
COPY ./requirements.txt ${DB_MANAGER_APP_DIR}requirements.txt
RUN pip install -r requirements.txt

COPY . ${DB_MANAGER_APP_DIR}

RUN chmod +x ${DB_MANAGER_APP_DIR}entrypoint.sh

CMD ${DB_MANAGER_APP_DIR}entrypoint.sh
