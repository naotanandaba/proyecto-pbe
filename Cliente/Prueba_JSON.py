import threading
import time
import urllib.request, json
import gi
import subprocess
from NFC import *
from py532lib.i2c import*
from py532lib.frame import*
from py532lib.constants import*
from py532lib.mifare import*

gi.require_version("Gtk","3.0")
from gi.repository import GLib, Gtk, Gdk, GObject

class Prueba_JSON:
    def data(self, query):
        print("http://192.168.1.63/"+query)
        with urllib.request.urlopen("http://192.168.1.63/"+query) as url:
            data = json.loads(url.read().decode())
            print(data)
        return data    
    