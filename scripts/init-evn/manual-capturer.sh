#!/bin/bash

#this script output window id, and mkdir by window name

info_str=`xwininfo | grep "Window id" | awk -F ' ' '{print $4 $5}' | sed -s "s/\"/ /g"`
echo $info_str
path=`echo "$info_str" | awk -F ' ' '{print $2}'`
full_path="/home/admin/flyingfish/"$path
mkdir -p $full_path
windowid=`echo $info_str | awk -F ' ' '{print $1}'`

while true
do
    filename=`date +%Y-%m-%d_%H:%M:%S.%N`
    xwd -id $windowid -out $full_path"/"$filename".xwd"
    convert $full_path"/"$filename".xwd" $full_path"/"$filename".png"
    rm $full_path"/"$filename".xwd"
    #
    sleep 0.7
    read TEMP
done

exit 0
