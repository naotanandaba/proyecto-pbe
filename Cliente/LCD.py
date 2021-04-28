import I2C_LCD_driver
from time import*

class LCD:
    def __init__ (self):
        self.mylcd = I2C_LCD_driver.lcd()
    def inicio (self,txt):
        self.mylcd.lcd_clear()
        #txt = "Aproxime su tarjeta"
        self.mylcd.lcd_display_string(txt,2)
    def nombre (self,txt1, txt2):
        self.mylcd.lcd_clear()
        #txt = "Aproxime su tarjeta"
        self.mylcd.lcd_display_string_pos(txt1,2,6)
        self.mylcd.lcd_display_string_pos(txt2,3,3)
