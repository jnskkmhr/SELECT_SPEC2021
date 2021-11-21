import sys 
import RPi.gpio as gpio 
import pigpio 
import smbus
import spidev
import time 
from math import pi 

import selemod 
from selemod import Actuator
from E2S import E2S
from EM_switch import EM_SW


class Resilience: 
    def __init__(self, DISTANCE:int, SPEC:dict): 
        """
        Args
        --------------------------------------------------------
        DISTANCE(int) : maximum altitude of climber (100m)
        SPEC(dict) : {"radius":radius(int), "height":height(int)}

        usage
        ---------------------------------------------------------------------------------
        set what's related to the mission (e.g. constants, class object, setup method etc)
        """
        # physical info about the climber 
        self.DISTANCE = DISTANCE
        self.REDUCE_RATE = 0.05 
        self.RADIUS, self.HEIGHT = SPEC["radius"], SPEC["height"]

        # pin setup 
        self.pin_esc = 18 
        self.pin_servo_1 = 23 
        self.freq_esc = 50 
        self.freq_servo = 50 
        self.brakeon_duty = 8.72
        self.brakeoff_duty = 4.85 
        self.throttle_a0 = 0.5 # duty vs throttle weight 
        self.throttle_a1 = 0.4 
        self.current_throttle = 90 
        self.target_throttle = 0 

        # motor motion setup 
        self.lower_lim = 0 
        self.middle_lim1 = 30 
        self.middle_lim2 = 60 
        self.upper_lim = 0.85 * self.DISTANCE 
        self.throttle1 = 90 
        self.throttle2 = 80 
        self.throttle3 = 60

        # e2s pin setup 
        self.pin_e2s_top = 16 
        self.pin_e2s_bottom = 20 

        # emergency switch pin setup 
        self.pin_em_sw = 21 

        # encoder pin setup & count, pos
        # these variable are crucial to the mission, so manage these as instance variable of class (do not use as an argument)
        self.counter = 0 
        self.pos = 0 
        

        self.actu = selemod.Actuator(pin_esc=self.pin_esc, pin_servo_1=self.pin_servo_1, 
                        freq_esc=freq_esc, freq_servo=freq_servo, 
                        brakeon_duty=brakeon_duty, brakeoff_duty=brakeoff_duty, 
                        throttle_a0=self.throttle_a0, throttle_a1=self.throttle_a1) #actuator(DC & servo motor)
        self.e2c = E2S(self.pin_e2s_top, self.pin_e2s_bottom) #E2S

        self.em_sw = EM_SW(self.pin_em_sw) #emergency switch 

        self.actu.calibrate_esc() #calibrate esc 
        self.actu.ser_1.brakeoff() #servo brake off b4 climbing 

    def motor(self, e2c_flag, em_flag): 
        """
        Arguments
        -------------------------------------------------------------------
        e2c_flag(tuple) : (top e2c flag, bottom e2c flag)
        em_flag(int) : binary flag(0/1) to notify if emergency switch is on 

        Usage
        ------------------------------------------------------------------------------------
        This method only changes throttle value based on encoder count vlaue. 
        Also stop motor based on counter value, e2s emergency signal, emergency switch signal
        """ 

        # suppose the entire path is categorized into 3 parts: begging, middle, ending
        # the user can create new category
        # if so, add position domain like middle_lim1, middle_lim2, middle_lim3, ... 
        # throttle value of each domain is initialized in construction 
        if self.lower_lim <= self.pos < self.middle_lim1: 
            self.target_throttle = throttle1
        elif self.middle_lim1 <= self.pos < self.middle_lim2: 
            self.target_throttle = throttle2
        elif self.middle_lim2 <= self.pos < self.upper_lim: 
            self.target_throttle = throttle3

        if self.current_throttle != self.target_throttle: #change throttle value only if current throttle and target throttle is different
            self.actu.new_throttle(self.target_throttle)
            self.current_throttle = self.target_throttle
        
        # if above, stop esc (this area is above safe zone, so immediately set throttle 0 once the climber reach this area)
        if self.upper_lim <= self.pos: 
            self.actu.stop_esc(self.current_throttle)
            print("switching to heli-mode")
            # cmd to switch to heli-mode 

        # E2S emergency stop 
        e2c_0_flag, e2c_1_flag = e2c_flag
        if e2c_0_flag == 0: 
            self.actu.stop_esc(self.current_throttle)
        if e2c_1_flag == 0: 
            self.actu.stop_esc(self.current_throttle)

        # Emergency switch stop 
        if em_flag == 0: 
            self.actu.stop_esc(self.current_throttle)
        else: 
            pass  
        
    def brake(self, servo_flag):
        """ 
        sevo_flag(int) : binary integer flag whether turning on brake or not 
        """
        if servo_flag==0: 
            self.actu.ser_1.brakeon()
        elif servo_flag==1: 
            self.actu.ser_2.brakeoff() 

    def _e2s(self): 
        e2s_0_flag = self.e2s.read_top()
        e2s_1_flag = self.e2s.read_bottom()
        return (e2s_0_flag, e2s_1_flag)

    
    def _em_sw(self): 
        em_flag = self.em_sw.read()
        return em_flag
    
    def _encoder(self): 
        '''based on encoder count value, compute climber's position'''
        # self.count = ... #update counter value here 
        self.pos = 2 * pi * self.RADIUS * self.count

    def run(self):
        # this is main program 


        