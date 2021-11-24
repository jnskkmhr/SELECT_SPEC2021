# suppose test.py is at the same directory as selemod.py 

#import dependencies 
import sys 
sys.path.append('../main')
from main import selemod 
import test_ec2 

# instantiate actuator class 
pin_esc = 18
pin_servo_1 = 23
# pin_servo_2 = 24
freq_esc = 50 
freq_servo = 50
brakeon_duty = 8.72 
brakeoff_duty = 4.85
throttle_a0 = 5.15
throttle_a1 = 0.047

pin_ec2_top = 16 
pin_ec2_bottom = 20

actu = selemod.Actuator(pin_esc=pin_esc, pin_servo_1=pin_servo_1, 
                        freq_esc=freq_esc, freq_servo=freq_servo, 
                        brakeon_duty=brakeon_duty, brakeoff_duty=brakeoff_duty,
                        throttle_a0=throttle_a0, throttle_a1=throttle_a1)

# initial setup of esc
print("Have you calibrated the motor? (y/n)")
yesorno = input() 
if yesorno == 'n':
    print("Start caliberation.")
    actu.calibrate_esc()
    print("Actuate motor. y/n")
    yesorno = input()
    if yesorno == 'y':
        try:
            #print("What throttle? Please type integer from 0 to 100.s")
            throttle = float(60)
            print("throttle_a0:", throttle_a0)
            print("throttle_a1:", throttle_a1)
            print("throttle:", throttle)
            # duty = throttle_a0 + throttle_a1 * throttle
            actu.new_throttle(throttle)
        except KeyboardInterrupt:
            print("Operation aborted. Duty ratio start decreasing.")
            # actu.stop_esc(duty)
            actu.stop_esc(throttle)
            print("Motor has stopped.")
    if yesorno == 'n':
        print("test aborted")

elif yesorno == 'y':
    print("Actuate motor. y/n")
    yesorno = input()
    if yesorno == 'y':
        try:
            #print("What throttle? Please type integer from 0 to 100.s")
            throttle = float(60)
            print("throttle_a0:", throttle_a0)
            print("throttle_a1:", throttle_a1)
            print("throttle:", throttle)
            # duty = throttle_a0 + throttle_a1 * throttle
            actu.new_throttle(throttle)

        except KeyboardInterrupt:
            print("Operation aborted. Duty ratio start decreasing.")
            # actu.stop_esc(duty)
            actu.stop_esc(throttle)
            print("Motor has stopped.")
    if yesorno == 'n':
        print("test aborted")


#throttle = [] #20 throttle points which correspond to 0~95 duty (5% increment -> 20data points)
#throttle_a0, throttle_a1 = actu.set_throttle(sampled_throttle)

# ec2 = test_ec2.EC2(pin_ec2_top, pin_ec2_bottom, actu)

# while True: 
#     actu.new_throttle(50)
#     ec2.read_top()
#     ec2.read_bottom()

# actu.end()