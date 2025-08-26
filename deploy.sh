#!/bin/bash

WSERVER="./wserver.sh"

#  exe server script
if [ -e "$WSERVER" ]; then
  chmod 755 $WSERVER
fi

docker compose up -d --build api


## run script in container
# $ docker exec -it api python script.py

## Remove All Unused Resources with Size Information:
# $ docker system df
# $ docker system prune -a --volumes -f

## find files by content
# find . -type d -name "node_modules" -prune -o -type f -name "*" -exec grep --color=auto -Hn "class" {} +


