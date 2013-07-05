#!/usr/bin/python
#

import sys, os

from gi.repository import Gtk,Gdk,GdkPixbuf,GLib

class CompositeUI:
    def __init__(self):
        handlers = {
            "cb_go_clicked": self.go,
            "cb_src_file_set": self.source_file_set,
            "cb_dest_file_set": self.dest_file_set,
            }
        self.builder = Gtk.Builder()
        self.builder.add_from_file('composite.ui')
        self.builder.connect_signals(handlers)
        self.mainWin = self.builder.get_object("mainWindow")
        self.srcWin = self.builder.get_object("sourceWindow")
        self.destWin = self.builder.get_object("destWindow")
        self.compWin = self.builder.get_object("compositeWindow")
        self.srcImg = self.builder.get_object("srcImage")
        self.destImg = self.builder.get_object("destImage")
        self.compImg = self.builder.get_object("compositeImage")
        self.mainWin.connect("destroy", Gtk.main_quit)
        self.mainWin.show()

    def go(self, widget):
        self.compositePixbuf = self.destPixbuf.copy()
        dest_x = int(self.builder.get_object("dest_x").get_text())
        dest_y = int(self.builder.get_object("dest_y").get_text())
        dest_width = int(self.builder.get_object("dest_width").get_text())
        dest_height = int(self.builder.get_object("dest_height").get_text())
        offset_x = float(self.builder.get_object("offset_x").get_text())
        offset_y = float(self.builder.get_object("offset_y").get_text())
        scale_x = float(self.builder.get_object("scale_x").get_text())
        scale_y = float(self.builder.get_object("scale_y").get_text())
        overall_alpha = float(self.builder.get_object("overall_alpha").get_text())
        self.srcPixbuf.composite(self.compositePixbuf,
                                 dest_x, dest_y,
                                 dest_width, dest_height,
                                 offset_x, offset_y,
                                 scale_x, scale_y,
                                 GdkPixbuf.InterpType.BILINEAR,
                                 overall_alpha)
        self.compImg.set_from_pixbuf(self.compositePixbuf)
        self.compWin.set_title("New Composite Image")
        self.compWin.show_all()

    def source_file_set(self, widget):
        try:
            self.srcPixbuf = GdkPixbuf.Pixbuf.new_from_file(widget.get_filename())
            self.srcImg.set_from_pixbuf(self.srcPixbuf)
            self.srcWin.set_title("SOURCE IMAGE: %dx%d" % (self.srcPixbuf.get_width(), self.srcPixbuf.get_height()))
            self.builder.get_object("dest_width").set_text(str(self.srcPixbuf.get_width()))
            self.builder.get_object("dest_height").set_text(str(self.srcPixbuf.get_height()))
            self.srcWin.move(self.mainWin.get_position()[0] + self.mainWin.get_size()[0], self.mainWin.get_position()[1])
            self.srcWin.show_all()
        except GLib.GError as e:
            print >>sys.stderr, e.message

    def dest_file_set(self, widget):
        try:
            self.destPixbuf = GdkPixbuf.Pixbuf.new_from_file(widget.get_filename())
            self.destImg.set_from_pixbuf(self.destPixbuf)
            self.destWin.set_title("DESTINATION IMAGE: %dx%d" % (self.destPixbuf.get_width(), self.destPixbuf.get_height()))
            self.destWin.move(self.mainWin.get_position()[0], self.mainWin.get_position()[1]  + self.mainWin.get_size()[1])
            self.destWin.show_all()
        except GLib.GError as e:
            print >>sys.stderr, e.message

if __name__ == '__main__':
    Gtk.init(None);
    ui = CompositeUI()
    Gtk.main()
