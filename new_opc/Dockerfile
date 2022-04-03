FROM python:3.10
ENV PYTHONUNBUFFERED=1 \
    BASE_HOST=0.0.0.0 \
    BASE_PORT=8000 \
    DB_ENGINE=django.db.backends.postgresql_psycopg2 \
    DB_NAME=postgres\
    DB_USER=mvlab\
    DB_PASSWORD=z1x2c3\
    DB_HOST=10.0.1.2\
    DB_PORT=5432\
    SUPERUSER_NAME=mvlab\
    SUPERUSER_EMAIL=info@mvlab.by\
    SUPERUSER_PASSWORD=z1x2c3\
    TZ=Europe/Minsk

WORKDIR /code
COPY requiremens.txt .
RUN pip3 install -r requiremens.txt
COPY . .
# RUN alembic revision --autogenerate
# RUN alembic upgrade head