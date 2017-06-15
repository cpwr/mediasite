FROM python:3.6-alpine

ENV INSTALL_DIR=/opt/mediasite
ENV PG_PORT: 5432
ENV PG_DB: mediasite
ENV PGDATA: /data
ENV PG_BIN: /usr/lib/postgresql/9.5/bin
ENV PG_USER: postgres
ENV PG_PASSWORD: postgres

RUN mkdir -p $INSTALL_DIR

WORKDIR $INSTALL_DIR

ADD . $INSTALL_DIR

RUN pip install -r $INSTALL_DIR/requirements.txt
RUN chown postgres:postgres $PGDATA;
su postgres -c "$PG_BIN/pg_ctl initdb" > /dev/null;
su postgres -c "$PG_BIN/pg_ctl -w -o '-F --port=$PG_PORT -k /tmp' start" > /dev/null;
su postgres -c "$PG_BIN/psql -h localhost -p $PG_PORT -c \"ALTER USER $PG_USER PASSWORD '$PG_PASSWORD'\"" > /dev/null;
su postgres -c "$PG_BIN/createdb -h localhost -p $PG_PORT $PG_DB -O $PG_USER" > /dev/null;
su postgres -c "$PG_BIN/psql -h localhost -p $PG_PORT -U $PG_USER -d $PG_DB -f db/schema.sql" > /dev/null;
rm /work/.dbcreation
sleep infinity

EXPOSE 8000

CMD python manage.py runserver -h 0.0.0.0 -p 8000
