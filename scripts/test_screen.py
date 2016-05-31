# -*- coding: utf-8 -*

from Screen import Screen
from Template_define import ScreenTemplates
from Tesseract import Tesseract
import os

conf = ScreenTemplates('/home/admin/volador/conf/feature_define.json')
tesseract = Tesseract()
templates = {}

#load templates
for k,v in conf.templates.iteritems():
    scrn = Screen(v.imgfile)
    for i in xrange(len(v.features)):
        scrn.loadFeature(v.features[i])
    templates[k] = scrn

#load screen pic 进行对比
test_path='/home/admin/volador/scripts/test_screen_pic/'

for f in os.listdir(test_path):
    tmp = os.path.join(test_path,f)
    if os.path.isfile(tmp):
        scr = Screen(tmp)
        ret = scr.matchTemplate(conf,templates,tesseract)
        print ret
