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
import gio, sqlite3, sql
import oper, gui, rss, feedparser

#Initialize-GUI

class callback(object):

  # Destroy application
  def destroy_main(self, widget):
    gtk.main_quit()
    
    
###################################################    
### OPML file import

### Callback fuction to show FileChooser
  def opml_import_show(self, widget):
    filter = gtk.FileFilter()
    filter.set_name('OPML')
    filter.add_pattern('*.opml')
    gui.appgui.opml_file_import.add_filter(filter)
    gui.appgui.opml_file_import.set_filter(filter)
    opml_response = gui.appgui.opml_file_import.run()
    if opml_response == 0 or opml_response == -4:
      gui.appgui.opml_file_import.hide()
      
### Callback function to hide the FileChooser on close
  def opml_import_hide(self, widget):
     gui.appgui.opml_file_import.hide()

### Callback function to import file to Feeds DIR
### If no file is selected and save button is clicked.. spawn 'no_file_error'
### If file already exists.. spawn 'import_error'
### ELSE copy selected file to Feeds DIR

  def opml_import(self, widget):
    gui.appgui.opml_file_import.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
    get_action = gui.appgui.opml_file_import.get_action()
    if get_action == gtk.FILE_CHOOSER_ACTION_SAVE:
      # Make sure Dipp directories exist
      oper.Tool.dipp_feeds_check()
      file = gui.appgui.opml_file_import.get_file()
      if file == None:
        no_file_response = gui.appgui.no_file_error.run()
        if no_file_response == 0 or no_file_response == gtk.RESPONSE_DELETE_EVENT:
          gui.appgui.no_file_error.hide()
          gui.appgui.opml_file_import.run()
      else:
        ## Get basname of "target" file..
        basename = file.get_basename()
        father = gio.File(path='Dipp/Subscriptions/Feeds')
        target = father.get_child(basename)
        #racy.. i know.
        result = target.query_exists()
        if result == True:
          warning_response = gui.appgui.import_error.run()
          if warning_response == -7 or warning_response == gtk.RESPONSE_DELETE_EVENT:
            gui.appgui.import_error.hide()
            gui.appgui.opml_file_import.run()
        elif result == False:
        #FIXME: when user tries to copy a directory - return ERROR
          test = file.copy(target)

### END OPML IMPORT ###
###################################################

###################################################
### Create a functon that is triggered by
### gtk.TreeSelection.get_selected and cause it to
### wipe tree_view2 and display feed data that is of
### the feed that is selected.

#FIXME
#FIXME
#FIXME




###################################################

###################################################
### Grab url from text entry/validate
### Parse with feed parser and collect realitive information
### Store information in DATABASE
### Pull information from DATABASE and display in Liststores


  def process_url(self, widget):

    link = gui.appgui.url_entry.get_text()
    gui.appgui.url_window.hide()
    feeds = feedparser.parse(link)
 
    if feeds['bozo'] == 1:
      url_error_show()

    else:
       text = ''
       gui.appgui.url_entry.set_text(text)
       ### Pull Title from feed
       ### Pull Entries from feed

       title = feeds.feed.title
       entries = feeds.entries
       
       ### Connect to DB and create a cursor
       conn = sqlite3.connect('.Dipp/DippDB')
       c = conn.cursor()

       ### Process up to #15 Entries pulling various data such as Title, Date, and of course the story itself.
       ### Last line inserts data in DB
       #'SELECT * FROM feeds WHERE feed_id=?', [])

       for story in entries[:25]:
          info = story.title_detail
          data = story.summary
          c.execute('INSERT INTO feeds VALUES (null, ?, ?, ?, ?, null)', \
          (story.updated, title, info.value, data))
          conn.commit()

       c.execute("SELECT title FROM Feeds WHERE id=?", [c.lastrowid])

       for row in c:
         iter = gui.appgui.list_store1.append()
         gui.appgui.list_store1.set (iter, 0, row[0])
         path = gui.appgui.tree_view1.get_selection()
         path.select_iter(iter)
         c.close()
    
       sql = "SELECT date, info FROM feeds"
       c.execute(sql)

       list_store2 = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
       gui.appgui.tree_view2.set_model(model=list_store2)

       for row in c:
         iter = list_store2.append()
         list_store2.set (iter, 0, row[0], 1, row[1])
       c.close()
       conn.close()





###################################################
### FEED LIST DATABASE EXPORT
### Create export dilalog that ask user if they want
### to'Save' their current feeds. 



### END
###################################################




###################################################
### NO FILE ERROR HIDE

### Callback to hide the 'no file selected' error message
  def no_file_hide(self, widget):
    gui.appgui.no_file_error.hide()

### END   
###################################################

###################################################
### URL WINDOW

### Callback function to spawn URL window and catch certin events.
  def url_window(self, widget):
    url_response = gui.appgui.url_window.run()
    if url_response == gtk.RESPONSE_DELETE_EVENT or url_response == gtk.RESPONSE_CANCEL:
      text = ''
      gui.appgui.url_entry.set_text(text)
      gui.appgui.url_window.hide()

### Callback funtion to hide the URL window on 'clicked' signal from button.     
  def url_window_hide(self, widget):
    text = ''
    gui.appgui.url_entry.set_text(text)
    gui.appgui.url_window.hide()


###################################################
### URL Invalid warning dialog hide

  def url_error_show(self):
    gui.appgui.url_entry.set_text('')
    url_response = gui.appgui.url_error.run()
    if url_response == gtk.RESPONSE_DELETE_EVENT or url_response == gtk.RESPONSE_CANCEL:
      gui.appgui.url_error.hide()

### Close button FC
###
  
  def url_error_hide(self, widget):
    gui.appgui.url_error.hide()


### END      
###################################################


###################################################
### ABOUT BOX


### Callback function to destroy about_box by user via menuitem13.
  def about_box(self, widget):
    about_response = gui.appgui.about_dialog.run()
    if about_response == gtk.RESPONSE_DELETE_EVENT or about_response == gtk.RESPONSE_CANCEL:
      gui.appgui.about_dialog.hide()

### END
###################################################      

### Statement to bind class 'Callback' to var name 'call'
call = callback()
