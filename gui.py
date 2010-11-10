#!/usr/bin/env python

import gtk
import sys
import gobject
import pango
import gtk.glade
import gtk.gdk
import pygtk
import gio
import oper
import fc, rss

#Initialize-GUI

class appgui(object):

#####################################
### Builder Object and Program_Version
    
    # connect application signals to call-back functions.
    dipp_v = 'Dipp v0.1 |'
    builder = gtk.Builder()
    builder.add_from_file('dipp_interface.glade')

#####################################
### Main Window : Menu
    
  
    main_window = builder.get_object('window1')
    main_window.connect('destroy', fc.call.destroy_main)
    
    gtk.rc_parse('themes/gtkrc')
    screen = main_window.get_screen()
    settings = gtk.settings_get_for_screen(screen)
    gtk.rc_reset_styles(settings)


    menu_one = builder.get_object('menu1')
    menu_one.item1_subitem7 = builder.get_object ('item1_subitem7')
    menu_one.item1_subitem7.connect('activate', fc.call.destroy_main)
    
    menu_one.item2_subitem1 = builder.get_object('item2_subitem1')
    menu_one.item2_subitem1.connect('activate', fc.call.url_window)
    
#####################################
### Load images into app. buttons

    image1 = builder.get_object('image1')
    image2 = builder.get_object('image2')
    image5 = builder.get_object('image5')
    image1.set_from_file('images/Down.png')
    image2.set_from_file('images/Up.png')
    image5.set_from_file('images/Flag.png')

#####################################
### OPML File Importer and Buttons

    #connect menu item 'Import opml feed' to callback function opml_show.
    # also cause 'opml_hide' to hide the window
    opml_file_import = builder.get_object('opml_file_import')
    opml_file_import.item1_subitem1 = builder.get_object('item1_subitem1')
    opml_file_import.item1_subitem1.connect('activate', fc.call.opml_import_show)
    opml_file_import.connect('close', fc.call.opml_import_hide)
    opml_file_import.connect('destroy', fc.call.opml_import_hide)
    
    # button1 runs opml_hide()
    opml_file_import.button1 = builder.get_object('button1')
    opml_file_import.button1.connect('clicked', fc.call.opml_import_hide)
    # button2 runs opml_save()
    opml_file_import.button2 = builder.get_object('button2')
    opml_file_import.button2.connect('clicked', fc.call.opml_import)

#####################################
### ERROR'S : 
# - Import Error
# - No File Error
        
    # hide warning_message on close : hide_warning()
    import_error = builder.get_object('import_error')
    import_error.connect('close', fc.call.opml_import_show)
    import_error.connect('destroy', fc.call.opml_import_show)
    
    no_file_error = builder.get_object('no_file_error')
    no_file_error.button9 = builder.get_object('button9')
    no_file_error.button9.connect('clicked', fc.call.no_file_hide)
    no_file_error.connect('destroy', fc.call.no_file_hide)

######################################
### URL Window and Entry 
### for FEED Links.
    
    url_window = builder.get_object('url_window')
    url_window.button5 = builder.get_object('button5')
    url_window.button5.connect('clicked', fc.call.process_url)
    url_window.button6 = builder.get_object('button6')
    url_window.button6.connect('clicked', fc.call.url_window_hide)
    
    url_entry = builder.get_object('entry2')

#######################################
### URL_Invalid dialog
### Dialog to spawn when user inserts invalid URL

    url_error = builder.get_object('url_error')
    url_error.button8 = builder.get_object('button8')
    url_error.button8.connect('clicked', fc.call.url_error_hide)

#######################################    
### Status Bar   

    status_bar = builder.get_object('statusbar')
    status_bar.push(1, dipp_v)

#######################################
### About Dialog
    
    about_dialog = builder.get_object('aboutdialog1')
    about_dialog.item5_subitem1 = builder.get_object ('item5_subitem1')    
    about_dialog.item5_subitem1.connect('activate', fc.call.about_box)
    
#######################################

### RSS Feed Reader
### Treeview 1, liststore 1 == Feed Title

    tree_view1 = builder.get_object('treeview1')
    cell = gtk.CellRendererText()
    column1 = gtk.TreeViewColumn('Feed', cell, text=0)
    tree_view1.append_column(column1)
    
    list_store1 = builder.get_object('liststore1')
    #list_store1.connect('row-inserted', fc.call.list_store2_update)


### Treeview 2, Liststore 2 == Feed Description

    tree_view2 = builder.get_object('treeview2')
    cell = gtk.CellRendererText()
    
    active = 1
    column = gtk.TreeViewColumn('Date', cell, text=0)
    column.set_clickable(active)
    
    column2 = gtk.TreeViewColumn('Subject', cell, text=1)
    column2.set_clickable(active)
    
    tree_view2.append_column(column)
    tree_view2.append_column(column2)
    #tree_view2.modify_font(pango.FontDescription("Droid Sans Mono 10"))
    list_store2 = builder.get_object('liststore2')
 
    
########################################
###-- Display application!
    main_window.show()

#-----End
