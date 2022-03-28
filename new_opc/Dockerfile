FROM python:3.10
ENV PYTHONUNBUFFERED=1 \
    BASE_HOST=0.0.0.0 \
    BASE_PORT=8000 \
    DB_ENGINE=django.db.backends.postgresql_psycopg2 \
    DB_NAME=db1\
    DB_USER=mvlab\
    DB_PASSWORD=z1x2c3\
    DB_HOST=10.0.1.1\
    DB_PORT=5432\
    SUPERUSER_NAME=mvlab\
    SUPERUSER_EMAIL=info@mvlab.by\
    SUPERUSER_PASSWORD=z1x2c3\
    TZ=Europe/Minsk

WORKDIR /code
COPY requiremens.txt .
RUN pip3 install -r requiremens.txt
COPY . .