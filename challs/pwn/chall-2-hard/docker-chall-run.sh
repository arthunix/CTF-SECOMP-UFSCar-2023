#!/bin/bash

docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker run --rm -it -d -p 22:2222 strange-people-knows-that-architecture
