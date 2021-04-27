import threading
import time
import numpy as np
from NFC import *
from Prueba_JSON import *
from gi.repository import GLib, Gtk, Gdk, GObject

class Fluido(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Cliente")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(500, 100)
        
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=15)
        self.add(self.hbox)
        
        self.box=Gtk.EventBox()
        self.box.override_background_color(0,Gdk.RGBA(0,0,8,1))
        self.label=Gtk.Label('<span foreground="white" size="x-large">Acerque su tarjeta universitaria</span>')
        self.label.set_use_markup(True)
        self.label.set_size_request(500,100) 
        self.box.add(self.label)
        
        self.button = Gtk.Button.new_with_label("Clear!")
        self.button.connect("clicked", self.on_clicked)

        self.hbox.pack_start(self.box, True, True, 0)
        self.hbox.pack_start(self.button, True, True, 0)
        self.entry = Gtk.Entry()
        
    
    def on_clicked(self, button):
        print("on_clicked")
        self.label.set_text("Acerque su tarjeta universitaria" )
        
        """
        cambia uid label
        bloquea el boton
        """
           
    def on_entry(self,entry):
         self.json.data(entry.get_text())
        #llama a un handler de NFC cuando se lee la tarjeta
        #habilitar boton clear
        #pasar a la pantalla de inicio
#adaptador que se encarga de invocar al read_uid del puzle1
    def on_tag(self,rdif,uid):
        print("ontag")
        self.label.set_text(uid)
        #habiliat el boton de logout
    def connect(self, signal, handler, *args):
        
        """
        conecto la señal(componente hijo) al handler
        si no pongo el . punto en el widget es que es de la super clase, Window
        si hay punto el connect se hace sobre el componente hijo
        """
class RfidReader:
    def __init__(self,rfid,handler):
  #      GLib.idle_add(self.run, handler)
        self.rfid = rfid
        self.handler=handler
        self.read_uid()
    def read_uid(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True 
        thread.start()
    def run(self):
        uid = self.rfid.read_uid()
        self.handler(self.rfid,uid)
if __name__ == "__main__":
    win = Fluido()
        #adaptador para leer de forma asincrona, que no se bloquee
    reader = RfidReader(NFC(),win.on_tag)
#con el clear.clcicked distingo el evento de pulsar el boton clear, vala para cualquier widget 
    win.connect("button.on_clicked", lambda uid_lector : reader.read_uid())
  #  win.connect("entry.activate", lambda entry_query : win.on_entry)     
 #   win.clear.emit("on_clicked")
    win.connect("destroy",Gtk.main_quit)
    win.show_all()
    Gtk.main()
    
