#!/bin/bash

set -e

docker build . -t chall_spawner -f Dockerfile
docker run --rm --env-file ../.env -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock --privileged --name chall_spawner chall_spawner