FROM python:3.4-alpine
ADD . /autotaglibro
WORKDIR . /autotaglibro

#app parameters
ARG DEBUG         #"True"
ARG SECRET_KEY    #"Hjuioh78687^%586h98jh98"
ARG DATABASE_URL  #"sqlite:///autotaglibro/db.sqlite3;"
ARG DEV_ENV       #"True"
ARG TelegramToken #"598551213:AAHVT4vMsBt_IUCrdvMyDsoTOSD5NoM0o1A"


RUN pip install -r requirements.txt
CMD ["python", "manage.py", "makemigrations"]
