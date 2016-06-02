#!/bin/bash
#这个脚本在人工指定窗口后，间隔1s自动捕获一次窗口，并发送通知消息

out_path="/home/admin/volador/screens/"
scripts_ptah="/home/admin/volador/scripts/"

#使用xwininfo 获取ubuntu窗口id
info_str=`xwininfo | grep "Window id" | awk -F ' ' '{print $4 $5}' | sed -s "s/\"/ /g"`
path=`echo "$info_str" | awk -F ' ' '{print $2}'`
full_path=$out_path$path
mkdir -p $full_path
windowid=`echo $info_str | awk -F ' ' '{print $1}'`

#向kafka发送消息通知event-processer
#msg format {"type":"tm-reg","role":"table-mstr","time":"2016-05-18 08:03:33","content":{"dev_name":"i4-成都紫荆-小艾妖","window_id":"0x5644"}}
time=`date +%Y-%m-%d\ %H:%M:%S`
msg="{\"type\":\"tm-reg\",\"role\":\"table-mstr\",\"time\":\"$time\",\"content\":{\"dev_name\":\"$path\",\"window_id\":\"$windowid\"}}"
#echo $msg
#exit 0

echo "$msg" | sh ${scripts_ptah}kafka-producer.sh event

#loop capture window
while true
do
    #filename=`date +%Y-%m-%d:%H:%M:%S`
    filename=`expr \`date +%s%N\` / 100000000`
    xwd -id $windowid -out $full_path"/"$filename".xwd"
    convert $full_path"/"$filename".xwd" $full_path"/"$filename".png"
    rm $full_path"/"$filename".xwd"
    #send kafka msg
    msg="{\"window_id\":\"${windowid}\",\"file_name\":\"${full_path}/${filename}.png\"}"
    echo "$msg" | sh ${scripts_ptah}kafka-producer.sh screen
    sleep 0.8
    #按一下键盘捕获当前界面
    read TEMP
done

exit 0
