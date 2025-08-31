#!/bin/bash

API_HOST=80.240.25.97
APP_PATH=/root/app/trebovanja-zoka-be--dbnj

scp ./.env root@$API_HOST:$APP_PATH
# scp ./db/.env root@$API_HOST:$APP_PATH/db
scp ./deploy-vars.sh root@$API_HOST:$APP_PATH
scp ./src/config/vars.py root@$API_HOST:$APP_PATH/src/config/vars.py
scp ./ngapp---iec2cy5qtf---dev-firebase-adminsdk-ynt8w-43abed87ff.json root@$API_HOST:$APP_PATH
# scp ./redis/redis.conf root@$API_HOST:$APP_PATH/redis
