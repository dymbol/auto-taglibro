FROM python:3.4-alpine
ADD . /autotaglibro
WORKDIR . /autotaglibro

#app parameters
#"True"
ARG DEBUG

#"Hjuioh78687^%586h98jh98"
ARG SECRET_KEY

 #"sqlite:///autotaglibro/db.sqlite3;"
ARG DATABASE_URL

#"True"
ARG DEV_ENV

#"598551213:AAHVT4vMsBt_IUCrdvMyDsoTOSD5NoM0o1A"
ARG TelegramToken


RUN pip install -r requirements.txt
CMD ["python", "manage.py", "makemigrations"]
