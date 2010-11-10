#!/usr/bin/env python

import gtk
import gobject
import pango
import gtk.glade
import gtk.gdk
import gui
import pygtk
import os
import oper
import fc, re, sqlite3
#--Initalize dipp-GUI

class dipp_init:

    if __name__ == "__main__":
      main = gui.appgui()

###############################################
#### Dipp directory checks...

      oper.Tool.dipp_dir_layout()


###############################################
#### Create Dipp DB

      newdir = os.path.expanduser('~')
      os.chdir(newdir)
      a = os.path.dirname('.Dipp/DippDB/')
      list = [a]
      for item in list:
        if not os.path.exists(item):
          conn = sqlite3.connect('.Dipp/DippDB')
          c = conn.cursor()
          test = c.execute('''create table Feeds(id INTEGER PRIMARY KEY, date INTEGER,
                              title TEXT, info TEXT, data TEXT, feed_id INTEGER)''')

          print '1st run: DB Created!'
          conn.commit()
          c.close()
          conn.close()
###############################################

      gtk.main()
