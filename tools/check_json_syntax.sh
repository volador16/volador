#!/bin/bash
#该脚本用于删除json文件中的注释，以便python json解析不会出错

file=$1

sed "/^ *\/\//d" $file > $file".tmp"

python /home/admin/volador/tools/json_syntax_check.py $file".tmp"
