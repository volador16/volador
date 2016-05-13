#!/bin/bash
#这个脚本帮助捕获基础特征界面，为后面的识别提供基础
#usage sh set-capture-windos.sh out-put-path

out_path=$1
#使用xwininfo 获取ubuntu窗口id
info_str=`xwininfo | grep "Window id" | awk -F ' ' '{print $4 $5}' | sed -s "s/\"/ /g"`
echo $info_str
path=`echo "$info_str" | awk -F ' ' '{print $2}'`
full_path=$out_path"/"$path
mkdir -p $full_path
windowid=`echo $info_str | awk -F ' ' '{print $1}'`

while true
do
    filename=`date +%Y-%m-%d_%H_%M_%S`
    xwd -id $windowid -out $full_path"/"$filename".xwd"
    convert $full_path"/"$filename".xwd" $full_path"/"$filename".png"
    rm $full_path"/"$filename".xwd"
    #按一下键盘捕获当前界面
    read TEMP
done

exit 0
