#Docker file used for testing purposes (Jenkins etc)

FROM mariadb
ENV MYSQL_ROOT_PASSWORD dev_password
ENV MYSQL_DATABASE autotaglibro


FROM ubuntu:18.04
ADD . /autotaglibro
WORKDIR . /autotaglibro

ENV DEBUG "True"
ENV DEV_ENV "False"   # if True, than uses sqlite db
ENV SECRET_KEY "guyhgyut6g%%%$ff453u"
ENV DATABASE_URL "mysql://autotaglibro:dev_password/autotaglibro"
ENV TelegramToken "598551213:AAHVT4vMsBt_IUCrdvMyDsoTOSD5NoM0o1A"

RUN apt-get update && apt-get  install -y python3 python3-pip postgresql-server-dev-all libmysqlclient-dev
RUN apt-get clean && apt-get autoclean && apt-get autoremove
RUN pip3 install -r /autotaglibro/requirements.txt
RUN pip3 install pylama

EXPOSE 8000
