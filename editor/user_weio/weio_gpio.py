def digitalWrite(pin, state) :
	"""Digital write will set voltage +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground"""
    pass
def digitalRead(pin) :
	"""Digital read will read actual voltage on corresponding pin. There are two possible answers : 0 if pin is connected to the Ground or 1 if voltage on the pin is higher than treshold of +2.4V.
	This function can be combined with activateInputPullup(pin) function that will activate internal 20K pullup resistor on corresponding pin. This is useful when sensor, like button, is connected
	to the pin, so there is no need for additional pullup resistors
	"""
    pass
def activateInputPullup(pin) :
	"""Activate input pullup function activates internal 20K pullup resistor on corresponding pin.  This is useful when sensor, like button, is connected to the pin, so there is no need for additional pullup resistors"""
	pass
def setPwmResolution(nBits) :
	"""Set pwm resolution function will set pwm value limit for pwm(pin,value) function in number of bits. For example 8bit corresponds to values from 0-255. This function will not affect hardware pwm function : hardwarePwm(pin, value)"""
    pass
def pwm(pin, value) :
	"""Pwm function or pulse with modulation function will simulate output of analog signals on corresponding pin. It generates square wave of specified duty cycle. It can be used to program a brightness of LED or 
	drive motor on various speeds. This function takes two parameters : pin number and it's value. If function setPwmResolution(nBits) is not called default value is 8bit resolution, that means values from 0-255.
	This function can be applied to all available pins on the card however this is an software pwm if higher frequency and better stability is needed use of hardwarePwm(pin,value) function is recommended."""
    pass
def hardwarePwm(pin, value) :
	"""Hardware pwm function or pulse with modulation function will simulate output of analog signals on corresponding pin. It generates square wave of specified duty cycle, approximately 490Hz. It can be used to program a brightness of LED or 
	drive motor on various speeds. This function takes two parameters : pin number and it's value. Value is expressed in 8bit or from 0-255. This function will not be affected with setPwmResolution(nBits) as it's limited 
	with hardware constrains. This is hardware implementation of pwm so it's available only on these pins : 3,5,6,9,10 and 11. If it's necessary to use pwm on all available pins see pwm(pin, value) function that drives
	software pwm."""
	pass
def analogRead(pin) :
	"""Analog read function reads input on specified Analog to Digital Convertor. ADC is available on pins A0,A1,A2,A3 and A4. Output is 10bits resolution or from 0-1023"""
    pass
def analogReference(reference):
	"""Analog reference function sets voltage maximum to ADC. That means that given voltage will be maximum of 10bits sampling. This function takes one parameter : INTERNAL, AREF, REGULAR"""
	pass
def shiftOut(dataPin, clockPin, bitOrder, value) :
	pass
def shiftIn(dataPin, clockPin, bitOrder) :
    pass
def pulseIn(pin, value, timeout) :
    pass
def getCurrentValueOfPin(pin) :
	"""This function returns current value that was set on specified pin"""
	pass