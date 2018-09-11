FROM ubuntu:18.04
ADD . /autotaglibro
WORKDIR . /autotaglibro


#"True"
ARG DEBUG
ENV DEBUG    ${DEBUG}

#"Hjuioh78687^%586h98jh98"
ARG SECRET_KEY
ENV SECRET_KEY ${SECRET_KEY}

 #"sqlite:///autotaglibro/db.sqlite3;"
ARG DATABASE_URL
ENV DATABASE_URL ${DATABASE_URL}

#"True"
ARG DEV_ENV
ENV DEV_ENV ${DEV_ENV}

#"598551213:AAHVT4vMsBt_IUCrdvMyDsoTOSD5NoM0o1A"
ARG TelegramToken
ENV TelegramToken ${TelegramToken}

RUN apt-get update && apt-get  install -y python3 python3-pip postgresql-server-dev-all
RUN pip3 install -r /autotaglibro/requirements.txt
RUN ["python3", "/autotaglibro/manage.py", "makemigrations"]
RUN ["python3", "/autotaglibro/manage.py", "migrate"]

CMD ["uwsgi", "--ini", "uwsgi.ini"]


EXPOSE 8000