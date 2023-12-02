#!/bin/bash

docker build -t i-forgot-to-patch-my-system .
docker run -d --rm -it -p 8080:80 i-forgot-to-patch-my-system
