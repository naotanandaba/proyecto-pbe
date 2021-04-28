
import threading
import time
from NFC import *
from Prueba_JSON import *
from gi.repository import GLib, Gtk, Gdk, GObject, Gio
import numpy as np
is_LCD_conected = False
if is_LCD_conected == True :
    from lcd import *
login_text = "Aproxime su tarjeta"

class Cliente(Gtk.Window):
    def __init__(self):
        self.lectura= True
        self.existente= False
        css_provider = Gtk.CssProvider()
            #Hemos de poner donde encontramos el archivo css
            #en mi caso esta en la misma carpeta que este
        css_provider.load_from_path("diseo.css")
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.nfc = NFC()
        self.json = Prueba_JSON()
        Gtk.Window.__init__(self, title="Cliente")
        self.set_default_size(500, 100)
        
        self.box3= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box3)

        self.box1= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box3.pack_start(self.box1,False,True,0)
        
        
        self.labelInicial=Gtk.Label()
        self.labelInicial.set_text(login_text)
        if is_LCD_conected == True :
            lcd.nombre(login_text)
        
        self.box1.pack_start(self.labelInicial,False,True,0)
        self.box1.set_homogeneous(True)
        self.buttonLogOut=Gtk.Button(label="Logout")
        self.buttonLogOut.connect("clicked", self.logout)
        self.box1.pack_end(self.buttonLogOut,False,True,3)
        self.buttonLogOut.set_sensitive(False)
                
        self.entry=Gtk.Entry()
        self.entry.set_text("Enter your Query!")
        self.box1.pack_start(self.entry,False,True,9)      
        self.entry.connect("activate",self.on_entry)
        self.entry.set_editable(False)
        
    def estado(self):
        while self.lectura == True:
            reader = RfidReader(NFC(),win.on_tag)
            self.lectura = reader.lectura
            self.existente = False
    def on_tag(self,rdif,uid):
        self.lectura= False
        self.entry.set_editable(False)
        self.buttonLogOut.set_sensitive(False)
        print("ontag")
        
        self.labelName=Gtk.Label()
        
        self.entry.set_editable(True)
        self.buttonLogOut.set_sensitive(True)

       # self.labelInicial.set_text(self.nfc.read_uid())
       # result = self.json.data(self.nfc.read_uid())
        result = self.json.data("students/?student=" + uid)
        if is_LCD_conected == True :
            lcd.nombre("Wellcome: ", uid)

        self.labelInicial.set_use_markup(True)
        self.labelInicial.set_label( 'Wellcome: '+'<span foreground="blue"> ' +result[0]['student_name']+'</span>')
        
        self.show_all()
    def on_entry(self,entry):
        if self.existente == True:
            self.box3.remove(self.box2)
            
        print("entry")
        data_json = self.json.data(entry.get_text())        
        self.create_table(entry.get_text())
        self.existente=True
    def create_table(self, data):        
        self.box2= Gtk.Box()
        self.box2.set_homogeneous(True)
        
        self.box3.pack_start(self.box2,False,True,0)
        self.box3.set_homogeneous(True)
        marks = np.array(["subject","name","mark"])
        timetables = np.array(["day","hour","subject","room"])
        tasks = np.array(["date","subject","name"])
        self.bbdd = np.array([marks,timetables,tasks])
        #bucle para poner la primera linea que es la de claves
        clave=data.split('?')[0]
        data_json= self.json.data(data)        
        #automatizamos el bucle de la primera fila para cualquier caso, no ha switch en python :'(        
        #clave tendrá que recogerla del entry y pasarla al if 
        if clave == "marks":
            id_clave=0
        if clave == "timetables":
            id_clave=1
        if clave == "tasks":
            id_clave=2
        self.table = Gtk.Table(n_rows=len(data_json),n_columns=len(self.bbdd[id_clave]),homogeneous=True)
        self.box2.pack_start(self.table,False,True,9)               
        for i in range(len(self.bbdd[id_clave])):
            self.labelFor=Gtk.Label()
            self.labelFor.set_text(self.bbdd[id_clave][i])
            self.table.attach(self.labelFor,i,i+1,0,1)       
        
        for i in range(len(data_json)):
            for j in range(len(self.bbdd[id_clave])):
                self.labelFor=Gtk.Label()
                self.labelFor.set_text(data_json[i][self.bbdd[id_clave][j]])
                self.table.attach(self.labelFor,j,j+1,i+1,i+2)
                if i%2 == 0:
                    self.labelFor.set_name("tb")
                else:
                    self.labelFor.set_name("tb1")
        self.show_all()
        self.existente=True
    def logout(self,buttonLogOut):
        self.lectura=True
        self.estado()
        self.box3.remove(self.box2)
        self.labelInicial.set_text("Aproxime su tarjeta")
        self.buttonLogOut.set_sensitive(False)
        self.entry.set_editable(False)
        self.resize(500, 100)
        self.show_all()
        
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
