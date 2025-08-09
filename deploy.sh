#!/bin/bash

WSERVER="./wserver.sh"

#  exe server script
if [ -e "$WSERVER" ]; then
  chmod 755 $WSERVER
fi

docker compose up -d --build api


#  run script inside container
# $ docker exec -it api python script.py

#  clean up unused containers, networks, and volumes:
# $ docker system prune -a
# $ docker system prune -a --volumes

#  search files by content
# $ find . -type d -name "node_modules" -prune -o -type f -name "*" -exec grep --color=auto -Hn "class" {} +

