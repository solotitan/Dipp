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
import gio, sqlite3, fc
import oper, gui, rss, feedparser

#Initialize-GUI

class sql(object):

  
  def  url_add(self):
       ### Connect to DB and create a cursor
       conn = sqlite3.connect('.Dipp/DippDB')
       c = conn.cursor()

       ### Process up to #15 Entries pulling various data such as Title, Date, and of course the story itself.
       ### Last line inserts data in DB
       #'SELECT * FROM feeds WHERE feed_id=?', [])

       title = fc.call.process_url.feeds.feed.title
       entries = fc.call.process_url.feeds.entries

       for story in entries[:25]:
          info = story.title_detail
          data = story.summary
          date = story.updated_parsed
          feed_date = date[:6]
          c.execute('INSERT INTO feeds VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, null)', \
          (date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min, date.tm_sec, title, info.value, data))
          conn.commit()

       #for item in entries[:25]:
          #date = item.updated_parsed
          #feed_date = [date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min, date.tm_sec]
          #c.execute('INSERT INTO feeds VALUES (null, ?, null, null, null, null)', [item])
       
       #conn.commit()

       c.execute("SELECT title FROM Feeds WHERE id=?", [c.lastrowid])

       for row in c:
         iter = gui.appgui.list_store1.append()
         gui.appgui.list_store1.set (iter, 0, row[0])
         path = gui.appgui.tree_view1.get_selection()
         path.select_iter(iter)
         c.close()
    
       sql = "SELECT year, month, day, hour, min, sec, info FROM feeds"
       c.execute(sql)

       list_store2 = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
       gui.appgui.tree_view2.set_model(model=list_store2)
       

       for row in c:
         iter = list_store2.append()
         list_store2.set (iter, 0, row[0:6], 1, row[6])
       c.close()
       conn.close()

tool = sql()


