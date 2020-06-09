#!/usr/bin/env bash



docker container exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --topic domains --create --partitions 2
docker container exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --topic urls --create --partitions 2
docker container exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --topic data --create --partitions 2