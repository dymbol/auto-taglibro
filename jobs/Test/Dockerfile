#Docker file used for testing purposes (Jenkins etc)

FROM mariadb
ENV MYSQL_ROOT_PASSWORD dev_password
ENV MYSQL_DATABASE autotaglibro


#FROM ubuntu:18.04 AS autotaglibro_server
ADD . /autotaglibro
WORKDIR . /autotaglibro

ARG DEBUG
ENV DEBUG "True"

ARG DEV_ENV
ENV DEV_ENV "False"   # if True, than uses sqlite db

ARG SECRET_KEY
ENV SECRET_KEY "guyhgyut6g%%%$ff453u"

ARG DATABASE_URL
ENV DATABASE_URL "mysql://autotaglibro:dev_password/autotaglibro"

ARG TelegramToken
ENV TelegramToken "598551213:AAHVT4vMsBt_IUCrdvMyDsoTOSD5NoM0o1A"

RUN apt-get update && apt-get  install -y python3 python3-pip postgresql-server-dev-all libmysqlclient-dev
RUN apt-get clean && apt-get autoclean && apt-get autoremove
RUN pip3 install pylama

EXPOSE 8000
