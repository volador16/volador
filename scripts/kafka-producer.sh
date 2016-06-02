#!/bin/bash
#该脚本用于向kafka指定的topic发消息
#usage: sh kafka-produceter.sh topic msg

kafka_path='/home/admin/3rd-volador/kafka_2.10-0.9.0.1/'
topic=$1

${kafka_path}bin/kafka-console-producer.sh --broker-list localhost:9092 --topic $topic
