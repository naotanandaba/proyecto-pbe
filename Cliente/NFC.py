from py532lib.i2c import*
from py532lib.frame import*
from py532lib.constants import*
from py532lib.mifare import*

class NFC:
    def __init__(self):
        self.pn532 = Mifare()  
        self.pn532.SAMconfigure()
    def read_uid(self):
        print("entro en nfc")
        #empiezo el hilo aquí
        card_data = self.pn532.scan_field()
        return card_data.hex().upper()


        