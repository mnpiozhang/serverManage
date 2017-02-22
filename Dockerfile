FROM python:2.7-slim

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		postgresql-client libpq-dev \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV DJANGO_VERSION 1.8.14

WORKDIR /usr/src/app
EXPOSE 8000

RUN pip install mysqlclient psycopg2 django=="$DJANGO_VERSION"  mongoengine=="0.11.0" paramiko=="1.17.3" tornado=="4.4.2"

CMD ["python", "run.py"]
