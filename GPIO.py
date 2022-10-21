import time
try:
    from RPLCD.i2c import CharLCD
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
class LED():
    def __init__(self,color=None,*args,** kwargs, ):
        self.pin = int(0)
        self.color = color
        self.state = False 
    def aktivieren(self,color):
        self.color = color
        if self.color == "gruen":
            self.pin = 21
        elif self.color == "gelb" == 20:
            self.pin = 20
        elif self.color == "rot":
            self.pin = 26
        GPIO.setup(self.pin, GPIO.OUT)
    
    def an(self):
        self.state = True
        GPIO.output(self.pin, GPIO.HIGH)

    def aus(self):
        self.state = False
        GPIO.output(self.pin, GPIO.LOW)
    
    def deaktivieren(self):
        GPIO.cleanup(self.pin)
class Sensor():
    def __init__(self,name,*args,**kwargs):
        self.name = name
        self.state = False

    def lesen(self):
      
        # 1-wire Slave Datei lesen
        file = open(f'/sys/bus/w1/devices/{self.name}')
        filecontent = file.read()
        file.close()
    
        # Temperaturwerte auslesen und konvertieren
        stringvalue = filecontent.split("\n")[1].split(" ")[9]
        temperature = float(stringvalue[2:]) / 1000
    
        # Temperatur ausgeben
        rueckgabewert = '%6.2f' % temperature 
        return(rueckgabewert)





class Display:
    def __init__(self):
        self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8, charmap='A02',
                           auto_linebreaks=True, backlight_enabled=True)
        self.displayinhalt = None
        self.displayhistory = []

    def schreiben(self, zeile1, zeile2=None):
        self.__set_displayinhalt(zeile1, zeile2)
        zeile1 = str(zeile1)
        self.lcd.clear()
        if zeile2 is None:
            self.lcd.write_string(zeile1)
        else:
            zeile2 = str(zeile2)
            if len(zeile1) > 16 or len(zeile2) > 16:
                self.lcd.write_string(zeile1)
                time.sleep(2)
                self.lcd.clear()
                self.lcd.write_string(zeile2)
                time.sleep(2)
            else:
                self.lcd.write_string(zeile1 + "\n\r" + zeile2)
Gruen = LED("gruen")
print(Gruen.aktivieren())
Gruen.ein()
Gruen.aus()
Gruen.deaktivieren()
Sen = Sensor("28-000004b9b8a7")
print(Sen.lesen())
display = Display()
display.schreiben("Hallo","display")

