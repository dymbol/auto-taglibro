#!/bin/bash
heroku run -a autotaglibro python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db.json
sed -i '1d' db.json
mv -f db.sqlite3 db.sqlite3.old
. export_dev_env_values.sh
python3 manage.py migrate
python3 manage.py loaddata db.json

rm -f db.json
rm -f db.sqlite3.old
