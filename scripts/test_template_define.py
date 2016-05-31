# -*- coding: utf-8 -*-

from Template_define import ScreenTemplates

st = ScreenTemplates('/home/admin/volador/conf/feature_define.json')
for k,v in st.templates.iteritems():
    print k
    print v.title
    print v.title_loc
    print v.imgfile
    print v.features
