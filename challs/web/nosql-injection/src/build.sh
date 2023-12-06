#!/bin/bash

git fetch
git clone

docker build -t nosql-injection . -f Dockerfile
docker tag nosql-injection:latest registry.ctf.secompufscar.com.br/nosql-injection:latest
docker push registry.ctf.secompufscar.com.br/nosql-injection:latest