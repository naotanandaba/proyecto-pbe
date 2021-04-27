import threading
import time
import numpy as np
from NFC import *
from Prueba_JSON import *
from gi.repository import GLib, Gtk, Gdk, GObject

class Fluido(Gtk.Window):
    def __init__(self):
        self.nfc = NFC() 
        Gtk.Window.__init__(self, title="Cliente")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(500, 100)
        
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=15)
        self.add(self.hbox)
        
        self.labelinicial = Gtk.Label("Aproxime su identificación!")
        self.add(self.labelinicial)
        entry=Gtk.Entry()
        entry.set_text("Enter your Query!")
        self.add(entry)
        self.hbox.pack_start(self.labelinicial, True, True, 0)
        self.hbox.pack_start(entry, True, True, 0)
    def on_tag(self):
        
        self.labelName.set_text(self.nfc.read_uid())
if __name__ == "__main__":
    win = Fluido()
        #adaptador para leer de forma asincrona, que no se bloquee
   # reader = RfidReader(NFC(),win.on_tag)
#con el clear.clcicked distingo el evento de pulsar el boton clear, vala para cualquier widget 
  #  win.connect("logOut.on_clicked", lambda uid_lector : reader.read_uid())
  #  win.connect("entry.activate", lambda entry_query : win.on_entry)
     
 #   win.clear.emit("on_clicked")
    win.connect("destroy",Gtk.main_quit)
    win.show_all()
    Gtk.main()