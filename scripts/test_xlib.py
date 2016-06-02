# -*- coding: utf-8 -*
from Xlib.display import Display
from Xlib import X

index = int(0)
def printWindowHierrarchy(window, indent):
    global index
    children = window.query_tree().children
    for w in children:
        if window.id == 0x3200004:
            #print(indent,'%x' %window.id,  window.get_wm_class() , window.get_wm_name())
            #print window.query_pointer()._data
            #print window.get_attributes()
            #print ("self.geometry", window.get_geometry())
            parent = window.query_tree().parent
            #print parent.query_pointer()._data
            #print ("parent.getmetry", parent.get_geometry())
            gp = parent.query_tree().parent
            #print gp.query_pointer()._data
            print ("gp.geometry", gp.get_geometry())
            ggp = gp.query_tree().parent
            print ("ggp.geometry", ggp.get_geometry())
            #window.configure(stack_mode=X.TopIf)
            window.set_input_focus(X.RevertToParent, X.CurrentTime)
            window.configure(stack_mode=X.Above)
            index += 1
            print "index=%d" %index
            #break
        print(indent,'%x' %window.id,  window.get_wm_class() , window.get_wm_name())
        printWindowHierrarchy(w, indent+'-')

display = Display(':0')
root = display.screen().root
printWindowHierrarchy(root, '-')

"""
display = Display(':0')
root = display.screen().root
children = root.query_tree().children
wantid = 0x4200004
vnc = None
for w in children:
    print "windowid=%x; wm_name=%s" %(w.id,w.get_wm_name())
    if w.id == wantid:
        print 'find window'
        print w.get_wm_name()
        break
"""
