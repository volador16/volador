#!/bin/bash
#这个脚本用于初始化kafka中的topic

topic_names="screen event"
kafka_path="/home/admin/3rd-volador/kafka_2.10-0.9.0.1"

cd $kafka_path
for tn in $topic_names
do
    bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic $tn
done
cd -
