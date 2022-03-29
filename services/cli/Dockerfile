FROM python:3.10.2-alpine

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/
COPY ./../db_manager/model /usr/src/app/model/

ENTRYPOINT ["python", "/usr/src/app/manage.py"]
