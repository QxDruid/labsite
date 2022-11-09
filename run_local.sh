#!/bin/bash
docker stop labsite_master
docker build -t labsite .
docker run -d -p127.0.0.1:8000:8000 --rm --name labsite_master -v /home/web_host/webserver/images/:/app/static/images/ --env-file /home/web_host/webserver/envfile labsite
