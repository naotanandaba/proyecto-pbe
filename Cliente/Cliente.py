import threading
import time
from NFC import *
from Prueba_JSON import *
from gi.repository import GLib, Gtk, Gdk, GObject, Gio
import numpy as np


class Cliente(Gtk.Window):
    def __init__(self):
        self.lectura= True
        css_provider = Gtk.CssProvider()
            #Hemos de poner donde encontramos el archivo css
            #en mi caso esta en la misma carpeta que este
        css_provider.load_from_path("diseño.css")
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.nfc = NFC()
        self.json = Prueba_JSON()
        Gtk.Window.__init__(self, title="Cliente")
        self.set_default_size(500, 100)
        
        self.vbox= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        
        self.hbox =Gtk.Box(spacing=3)        
        self.vbox.pack_start(self.hbox,True,True,0)
        
        self.labelInicial=Gtk.Label()
        self.labelInicial.set_text("Aproxime su tarjeta")
        self.hbox.pack_start(self.labelInicial,False,True,0)
        
        self.buttonLogOut=Gtk.Button(label="Logout")
        self.buttonLogOut.connect("clicked", self.logout)
        self.hbox.pack_end(self.buttonLogOut,False,True,3)
        self.buttonLogOut.set_sensitive(False)
                
        self.entry=Gtk.Entry()
        self.entry.set_text("Enter your Query!")
        self.vbox.pack_start(self.entry,False,True,9)      
        self.entry.connect("activate",self.on_entry)
        self.entry.set_editable(False)
        
        self.table = Gtk.Table(n_rows=0,n_columns=0,homogeneous=True)
        self.vbox.pack_start(self.table,False,True,9)
        self.table.hide()
        
    def estado(self):
        while self.lectura == True:
            reader = RfidReader(NFC(),win.on_tag)
            self.lectura = reader.lectura
        
    def on_tag(self,rdif,uid):        
        self.entry.set_editable(False)
        self.buttonLogOut.set_sensitive(False)
        print("ontag")
        
        self.labelName=Gtk.Label()
        result = self.json.data(uid)
        
        self.entry.set_editable(True)
        self.buttonLogOut.set_sensitive(True)

       # self.labelInicial.set_text(self.nfc.read_uid())
       # result = self.json.data(self.nfc.read_uid())
        self.labelInicial.set_text("Wellcome: "+result)
                
        print("llega")
    def on_entry(self,entry):
        print("entry")
        self.table.show()
        data_json = self.json.data(entry.get_text())
        
        marks = np.array(["subject","name","mark"])
        timetables = np.array(["Day","Hour","Subject","Room"])
        tasks = np.array(["Date","Subject","Name"])
        bbdd = np.array([marks,timetables,tasks])
        #bucle para poner la primera linea que es la de claves
        clave = "marks"
        
        #automatizamos el bucle de la primera fila para cualquier caso, no ha switch en python :'(        
        #clave tendrá que recogerla del entry y pasarla al if 
        if clave == "marks":
            id_clave=0
        if clave == "timetables":
            id_clave=1
        if clave == "tasks":
            id_clave=2
       
        self.table.resize(len(data_json),len(bbdd[id_clave]))
                
        for i in range(len(bbdd[id_clave])):
            labelFor=Gtk.Label()
            labelFor.set_text(bbdd[id_clave][i])
            self.table.attach(labelFor,i,i+1,0,1)        
        #bucle para llenar la table 
        for i in range(len(data_json)):
            for j in range(len(bbdd[id_clave])):
                labelFor=Gtk.Label()
                labelFor.set_text(data_json[i][bbdd[id_clave][j]])
                self.table.attach(labelFor,j,j+1,i+1,i+2)
                if i%2 == 0:
                    labelFor.set_name("tb")
                else:
                    labelFor.set_name("tb1")
       # self.json.data(entry.get_text())
    def create_table(self, data_json):
        print()
        
    def logout(self,buttonLogOut):
        self.lectura=True
        self.estado()
        self.labelInicial.set_text("Aproxime su tarjeta")
        print("logout")
        
class RfidReader:
    def __init__(self,rfid,handler):
  #      GLib.idle_add(self.run, handler)
        self.rfid = rfid
        self.handler=handler
        self.read_uid()
        self.lectura=False
    def read_uid(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True 
        thread.start()
    def run(self):
        uid = self.rfid.read_uid()
        self.handler(self.rfid,uid)
        
if __name__ == "__main__":
    win = Cliente()
    win.estado()
    win.connect("destroy",Gtk.main_quit)
    win.show_all()
    Gtk.main()