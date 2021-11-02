import selemod 
import pigpio
import test_ec2

actu = selemod.Actuator(pin_esc=12, pin_servo_1=8, pin_servo_2=7, 
                        freq_esc=50, freq_servo=70, brakeon_duty=13.3, 
                        brakeoff_duty=7, throttle_a0=7.5555, throttle_a1=0.027
                        )


#initial setup of esc
actu.test_esc()
throttle = [] #20 throttle points which correspond to 0~95 duty (5% increment -> 20data points)
throttle_a0, throttle_a1 = actu.set_throttle(sampled_throttle)

ec2 = test_ec2.EC2(pin_ec2_top, pin_ec2_bottom, actu)

while True: 
    actu.new_throttle(50)
    ec2.read_top()
    ec2.read_bottom()

actu.end()