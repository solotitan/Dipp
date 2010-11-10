#!/usr/bin/env python

import gtk
import sys
import gobject
import pango
import gtk.glade
import gtk.gdk
import pygtk
import os
import shutil
import gio, sqlite3

#Initialize-GUI

class tool(object):

  def dipp_dir_layout(self):
    newdir = os.path.expanduser('~')
    os.chdir(newdir)
    a = os.path.dirname('Dipp/')
    b = os.path.dirname('Dipp/Plugins/')
    c = os.path.dirname('Dipp/Themes/')
    d = os.path.dirname('Dipp/Subscriptions/')
    e = os.path.dirname('Dipp/Subscriptions/Feeds/')
    f = os.path.dirname('.Dipp/')
    list = [a,b,c,d,e,f]
    for item in list:
      if not os.path.exists(item):
        os.makedirs(item)
    

  def dipp_feeds_check(self):
    newdir = os.path.expanduser('~')
    os.chdir(newdir)
    d = os.path.dirname('Dipp/Subscriptions/Feeds/')
    if not os.path.exists(d):
      os.makedirs(d)
    else:
      path = os.getcwd()
      
      
Tool = tool()
