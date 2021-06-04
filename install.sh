#!/bin/bash

# очищаем старый образ и сеть
docker rmi flask_app
docker network rm flask_app_net

#билд образа flask
docker build -t flask_app .
#создаем сеть для соединения контейнеров flask и nginx
docker network create flask_app_net
# запускаем образ flask
docker run -d --name flaskapp --net flask_app_net -p8000:8000 -p465:465 --env-file .env -v ~/webserver/static:/app/static -v ~/webserver/database:/database flask_app
# запускаем nginx
docker run -d --name nginx --net flask_app_net -p80:80 -v ~/webserver/config:/etc/nginx/conf.d nginx