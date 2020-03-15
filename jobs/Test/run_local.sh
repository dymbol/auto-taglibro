#/usr/bin/env bash
# Use that dockerfile to run this code locally, and access it using http://127.0.0.1:8000
####################
set -x
SCRIPT_DIR="$(dirname "$0")"
BUILD_DIR="$SCRIPT_DIR/../../"
####################

mkdir -p /tmp/at_logs
mkdir -p /tmp/at_docs

docker build -t autotaglibro  \
    --build-arg DEBUG=True \
    --build-arg SECRET_KEY="Hjuioh78687^%586h98jh98" \
    --build-arg DATABASE_URL="sqlite:///autotaglibro/db.sqlite3;" \
    --build-arg DEV_ENV="True" \
    --build-arg TelegramToken="598551213:AAHVT4vMsBt_IUCrdvMyDsoTOSD5NoM0o1A" $BUILD_DIR


docker run  -it  -v /tmp/at_logs:/autotaglibro_logs \
-v /tmp/at_docs:/autotaglibro/auto-taglibro/journal/static/car_files \
-e "ALLOWED_HOSTS=127.0.0.1" \
-p 8000:8000 autotaglibro





