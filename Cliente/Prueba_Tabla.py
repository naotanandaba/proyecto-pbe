import threading
import time
import numpy as np
from NFC import *
from Prueba_JSON import *
import gtk.gdk
from gi.repository import GLib, Gtk, Gdk, GObject

class Tabla(Gtk.Window):
    def __init__(self):       
        Gtk.Window.__init__(self, title="Tabla")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(500, 100)
        self.json = Prueba_JSON()
     #   data = json.loads('[{"subject":"AST","name":"control teoria","mark":"7.5"},{"subject":"AST","name":"final","mark":"8.6"},{"subject":"PBE","name":"Puzle2","mark":"8.4"},{"subject":"PBE","name":"control","mark":"7.3"}]')
    #    data_json = data       
        
        data_json = self.json.data("?mark[lt]=4")#recoger la query del entry 
        
        vbox= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)
        
        hbox =Gtk.Box(spacing=3)        
        vbox.pack_start(hbox,True,True,0)
        
        labelName=Gtk.Label()
        labelName.set_text("Wellcome: Jose Antonio")
        hbox.pack_start(labelName,False,True,0)
        self.buttonLogOut=Gtk.Button(label="Logout")
        self.buttonLogOut.connect("clicked", self.on_button_clicked)
        hbox.pack_end(self.buttonLogOut,False,True,3)
        
        entry=Gtk.Entry()
        entry.set_text("Enter your Query!")
        vbox.pack_start(entry,False,True,9)      
        entry.connect("activate",self.on_entry)
        
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

        table = Gtk.Table(rows=len(data_json),columns=len(bbdd[id_clave]),homogeneous=True)
        vbox.pack_start(table,False,True,9)
                
        for i in range(len(bbdd[id_clave])):
            labelFor=Gtk.Label()
            labelFor.set_text(bbdd[id_clave][i])
            table.attach(labelFor,i,i+1,0,1)        
        #bucle para llenar la table 
        for i in range(len(data_json)):
            for j in range(len(bbdd[id_clave])):
                labelFor=Gtk.Label()
                labelFor.set_text(data_json[i][bbdd[id_clave][j]])
                table.attach(labelFor,j,j+1,i+1,i+2)
                if i%2 == 0:
                    labelFor.set_name("tb")
                else:
                    labelFor.set_name("tb1")
        #Diseño de la ventana
        css_provider = Gtk.CssProvider()
            #Hemos de poner donde encontramos el archivo css
            #en mi caso esta en la misma carpeta que este
        css_provider.load_from_path("diseño.css")
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
                
        self.show_all()
        Gtk.main()
    def on_button_clicked(self,buttonLogOut):
         print("Entro al boton")
    def update_progess(self):
        buffer = self.entry.get_buffer()
        startIter, endIter = buffer.get_bounds()
        text = buffer.get_text(startIter, endIter, False)
        print(text)
    def on_entry(self,entry):
         self.json.data(entry.get_text())
         
         
win = Tabla()