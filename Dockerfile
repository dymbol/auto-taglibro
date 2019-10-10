#Docker file used for testing purposes (Jenkins etc)
FROM ubuntu:18.04
ADD . /autotaglibro
WORKDIR /autotaglibro

ARG MYSQL_HOST
ENV MYSQL_HOST=${MYSQL_HOST}
ARG MYSQL_USER
ENV MYSQL_USER=${MYSQL_USER}
ARG MYSQL_PASSWORD
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}
ARG MYSQL_PORT
ENV MYSQL_PORT=${MYSQL_PORT}
ARG MYSQL_DATABASE
ENV MYSQL_DATABASE=${MYSQL_DATABASE}

ARG ALLOWED_HOSTS
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}

# "True" or "False"
ARG DEBUG
ENV DEBUG=${DEBUG}

#"False" # if True, than uses sqlite db
ARG DEV_ENV
ENV DEV_ENV=${DEV_ENV}

#"guyhgyut6g%%%$ff453u"
ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

ENV DATABASE_URL=mysql://$MYSQL_USER:$MYSQL_PASSWORD@$MYSQL_HOST:$MYSQL_PORT/$MYSQL_DATABASE

#"598551213:AAHVT4vMsBt_IUCrdvMyDsoTOSD5NoM0o1A"
ARG TelegramToken
ENV TelegramToken={$TelegramToken}

RUN apt-get update && apt-get  install -y python3 python3-pip postgresql-server-dev-all libmysqlclient-dev mariadb-client
RUN apt-get clean -y && apt-get autoclean -y && apt-get autoremove -y

RUN pip3 install -r requirements.txt
RUN python3 manage.py migrate
RUN echo yes | python3 manage.py collectstatic

EXPOSE 8000

CMD demo/create_admin.py | python3 manage.py shell && python3 manage.py runserver 0.0.0.0:8001
