#Docker file used for testing purposes (Jenkins etc)
FROM ubuntu:18.04
ADD . /autotaglibro
WORKDIR . /autotaglibro

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

# "True" or "False"
ARG DEBUG
ENV DEBUG=${DEBUG}

#"False" # if True, than uses sqlite db
ARG DEV_ENV
ENV DEV_ENV=${DEV_ENV}

#"guyhgyut6g%%%$ff453u"
ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

#"mysql://autotaglibro_tests:dev_password@127.0.0.1/autotaglibro_tests"
ENV DATABASE_URL=mysql://${MYSQL_DATABASE}:${MYSQL_PASSWORD}@${MYSQL_HOST}/${MYSQL_DATABASE}

#"598551213:AAHVT4vMsBt_IUCrdvMyDsoTOSD5NoM0o1A"
ARG TelegramToken
ENV TelegramToken={$TelegramToken}

RUN apt-get update && apt-get  install -y python3 python3-pip postgresql-server-dev-all libmysqlclient-dev
RUN apt-get clean -y && apt-get autoclean -y && apt-get autoremove -y
RUN pip3 install pylama
