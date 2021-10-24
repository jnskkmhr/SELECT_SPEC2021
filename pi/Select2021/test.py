# suppose test.py is at the same directory as selemod.py 

#import dependencies 
import selemod 

# instantiate actuator class 
pin_esc = 12
pin_servo_1 = 13
pin_servo_2 = 18 
freq_esc = 50 
freq_servo = 1000 

actu = selemod.Actuator(pin_esc=pin_esc, pin_servo_1=pin_servo_1, pin_servo_2=pin_servo_2, freq_esc=freq_esc, freq_servo=freq_servo)
actu.test_esc()