#!/bin/bash

set -e

docker build -t container-spawner .
docker tag container-spawner:latest registry.ctf.secompufscar.com.br/container-spawner:latest
docker push registry.ctf.secompufscar.com.br/container-spawner:latest
