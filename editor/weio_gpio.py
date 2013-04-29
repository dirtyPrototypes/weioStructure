import os

def pinMode(pin, dir) :
    s_pin = str(pin)
    inputFile = open("/sys/class/gpio/export", "w")
    rep = inputFile.write(s_pin)
    inputFile.close()
    if os.path.exists("/sys/devices/virtual/gpio/gpio" + s_pin + "/direction") :
        inputFile = open("/sys/devices/virtual/gpio/gpio" + s_pin + "/direction", "w")
        rep = inputFile.write(dir)
        inputFile.close()
    else :
        print "WEIO says : pin " + str(pin) + " is busy or non existant"

def digitalWrite(pin, state) :
    if os.path.exists("/sys/devices/virtual/gpio/gpio" + str(pin) + "/value") :
        inputFile = open("/sys/devices/virtual/gpio/gpio" + str(pin) + "/value", "w")
        rep = inputFile.write(state)
        inputFile.close()
    print "WEIO says : pin " + str(pin) + " is not accessible, did you declare pinmode(pin, direction)?"
        
def digitalRead(pin) :
    if os.path.exists("/sys/devices/virtual/gpio/gpio" + str(pin) + "/value") :
        inputFile = open("/sys/devices/virtual/gpio/gpio" + str(pin) + "/value", "r")
        rep = inputFile.read()
        return rep
    else :
        print "WEIO says : pin " + str(pin) + " is not accessible, did you declare pinmode(pin, direction)?"
        return None
