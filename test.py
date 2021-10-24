# suppose test.py is at the same directory as selemod.py 

#import dependencies 
import selemod 

pin_esc = 12
pin_servo_1 = 8
pin_servo_2 = 7 
freq_esc = 50 
freq_servo = 1000 
brakeon_duty = 5.0 
brakeoff_duty = 5.0 

actu = selemod.Actuator(pin_esc=pin_esc, pin_servo_1=pin_servo_1, pin_servo_2=pin_servo_2, freq_esc=freq_esc, freq_servo=freq_servo, brakeon_duty=brakeon_duty, brakeoff_duty=brakeoff_duty)

actu = selemod.Actuator(pin_esc=12, pin_servo_1=8, pin_servo_2=7, freq_esc=50, freq_servo=70, brakeon_duty=13.3, brakeoff_duty=7, throttle_a0=7.5555, throttle_a1=0.027)

actu.test_esc()