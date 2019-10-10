# auto-taglibro
Car maintanance scheduler

```
python3 manage.py migrate
python3 manage.py createsuperuser
```

You need to pass environment variables for particular environment (like: $ export SECRET_KEY="ggu7t6rg737&*(%6*" ):

PROD environment (Heroku)

 * SECRET_KEY      #by Heroku panel
 * DATABASE_URL    #by Heroku panel
 * DEBUG=True;     #True or False by Heroku panel
 * DEV_ENV=True

DEV environment:

 * SECRET_KEY      #string with secret key
 * DATABASE_URL    #example: sqlite:////home/dymbol/GIT/Github/auto-taglibro/db.sqlite3;
 * DEBUG           #True or False
 * DEV_ENV=True

You can simply build docker image:
```
docker build -t autotaglibro  \
    --build-arg DEBUG=True \
    --build-arg SECRET_KEY="Hjuioh78687^%586h98jh98" \
    --build-arg DATABASE_URL="sqlite:///autotaglibro/db.sqlite3;" \
    --build-arg DEV_ENV="True" \
    --build-arg TelegramToken="598551213:AAHVT4vMsBt_IUCrdvMyDsoTOSD5NoM0o1A" .
docker run  -d  -v /host_dir_logs:/autotaglibro_logs \
-v /host_docs_dir:/autotaglibro/auto-taglibro/journal/static/car_files \
-e "ALLOWED_HOSTS=127.0.0.1" \
-p 8000:8000 autotaglibro
```
and use your browser with address http://127.0.0.1:8000
