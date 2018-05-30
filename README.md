# auto-taglibro
Car maintanance scheduler

1. python3 manage.py migrate
2. python3 manage.py createsuperuser


You need to pass environment variables for particular environment (like: $ export SECRET_KEY="ggu7t6rg737&*(%6*" ):
    PROD environment (Heroku)
        SECRET_KEY      #by Heroku panel
        DATABASE_URL    #by Heroku panel
        DEBUG=True;     #True or False by Heroku panel
        DEV_ENV=True
    DEV environment:
        SECRET_KEY      #string with secret key
        DATABASE_URL    #example: sqlite:////home/dymbol/GIT/Github/auto-taglibro/db.sqlite3;
        DEBUG           #True or False
        DEV_ENV=True