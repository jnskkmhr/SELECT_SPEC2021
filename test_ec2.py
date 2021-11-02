import Rpi.gpio as GPIO
import time

#このプログラムの起動は時限式にする
# もしくは、クライマーの高度が上端のダンパー付近に来た時に、起動する

GPIO.setmode(GPIO.BCM)

pin_ec2_top = 16 
pin_ec2_bottom = 20


class EC2:
    def __init__(self, pin_ec2_top, pin_ec2_bottom, esc, ser): 
        """
        Argument
        ------------------------------------------
        pin_ec2top_ : ec2 corrector gpio
        pin_ec2_bottom : bottom ec2 corrector gpio 
        esc : esc instance (GPIO.PWM)
        ser : servo instance (GPIO.PWM)
        """
        self.pin_ec2_top = pin_ec2_top 
        self.pin_ec2_bottom = pin_ec2_bottom 
        self.esc = esc 
        self.ser = ser 
        GPIO.setup(pin_ec2_top, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(pin_ec2_bottom, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    def read_top(self): 
        top_sw_state = GPIO.input(self.pin_ec2_top)

        if GPIO.input(self.pin_ec2_top): 
            print("Top Switch ON")
            ## cut off pwm signal here ##
            self.esc.stop()
            self.ser.stop()
            print("cutting off pwm and servo signal")
            time.sleep(1)
        else: 
            pass

    def read_bottom(self): 
        top_sw_state = GPIO.input(self.pin_ec2_bottom)

        if GPIO.input(self.pin_ec2_bottom): 
            print("Bottom Switch ON")
            ## cut off pwm signal here ##
            self.esc.stop()
            self.ser.stop()
            print("cutting off pwm and servo signal")
            time.sleep(1)
        else: 
            pass 

    def destoy(self): 
        GPIO.cleanup()
