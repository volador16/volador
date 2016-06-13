# -*- coding: utf-8 -*-
"""
这个脚本用于测试json配置文件语法是否OK
@author: volader
"""
import json
import sys

if len(sys.argv) != 2:
    print "usage python json_syntax_check.py json-file"
    print "check input!"
    exit()
print sys.argv
jsonfile = sys.argv[1]
fl = file(jsonfile)
json.load(fl)
