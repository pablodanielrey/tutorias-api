#!/bin/bash
docker run -ti --rm --name mongo-express --add-host mongo:192.168.0.56 -p 8081:8081 mongo-express
