import RPi.gpio as gpio 
import time 

class EM_SW:
    def __init__(self, pin_em_sw): 
        """
        Argument
        ------------------------------------------
        pin_em_sw : emergency switch signal gpio 
        """
        self.pin_em_sw = pin_em_sw
        GPIO.setup(pin_e2s_top, GPIO.IN) #switch is connected with pull-up resistor, so disable Raspberry pi's internal pull up 
    
    def read(self): 
        top_sw_state = GPIO.input(self.pin_em_sw)

        if GPIO.input(self.pin_em_sw): 
            return 1
        else: 
            print("Emergency switch ON")
            return 0  

    def destoy(self): 
        GPIO.cleanup()