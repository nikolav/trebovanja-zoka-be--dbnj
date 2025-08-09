#!/bin/bash

WSERVER="./wserver.sh"

#  exe server script
if [ -e "$WSERVER" ]; then
  chmod 755 $WSERVER
fi

docker compose up -d --build api


# docker exec -it api python script.py

# find . -type d -name "node_modules" -prune -o -type f -name "*" -exec grep --color=auto -Hn "class" {} +
