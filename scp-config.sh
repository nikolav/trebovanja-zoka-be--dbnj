#!/bin/bash

API_HOST=45.76.91.37
APP_PATH=/root/app/flaskapp

scp ./.env root@$API_HOST:$APP_PATH
# scp ./db/.env root@$API_HOST:$APP_PATH/db
scp ./deploy-vars.sh root@$API_HOST:$APP_PATH
scp ./src/config/vars.py root@$API_HOST:$APP_PATH/src/config/vars.py
scp ./ngapp---iec2cy5qtf---dev-firebase-adminsdk-ynt8w-78ca6332f5.json root@$API_HOST:$APP_PATH
# scp ./redis/redis.conf root@$API_HOST:$APP_PATH/redis
