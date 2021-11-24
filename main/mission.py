import sys 
import RPi.GPIO as gpio 
import pigpio 
import smbus
import spidev
import time 
from math import pi 

import selemod 
from selemod import Actuator, Bme280, Sht31
from E2S import E2S
from EM_switch import EM_SW

import threading # if unable to import, use "pip3 install thread6 in terminal"


class Resilience: 
    def __init__(self, DISTANCE:int, SPEC:dict, sensor:dict): 
        """
        Args
        --------------------------------------------------------
        DISTANCE(int) : maximum altitude of climber (100m)
        SPEC(dict) : {"radius":radius(int), "height":height(int)}
        sensor(dict) : {"bme" : bool, "sht" : bool}

        usage
        ---------------------------------------------------------------------------------
        set what's related to the mission (e.g. constants, class object, setup method etc)
        """

        # mode of esc 
        # 0 => elevation  1 => free fall 
        self.mode = 0 

        # physical info about the climber 
        self.DISTANCE = DISTANCE
        self.REDUCE_RATE = 0.05 
        self.RADIUS, self.HEIGHT = SPEC["radius"], SPEC["height"]
        self.bme_is_use, self.sht_is_use = sensor["bme"], sensor["sht"]

        # pin setup 
        self.pin_esc = 18 
        self.pin_servo_1 = 23 
        self.freq_esc = 50 
        self.freq_servo = 50 
        self.brakeon_duty = 8.72
        self.brakeoff_duty = 4.85 
        self.throttle_a0 = 5.15 # duty vs throttle weight 
        self.throttle_a1 = 0.047 
        self.current_throttle = 0
        self.target_throttle = 0 

        # motor motion setup 
        self.lower_lim = 0 
        self.middle_lim1 = 0.3 * self.DISTANCE
        self.middle_lim2 = 0.5 * self.DISTANCE
        self.upper_lim = 0.85 * self.DISTANCE 
        self.throttle1 = 60 
        self.throttle2 = 60 
        self.throttle3 = 50
        self.throttle_const = 40 # if heli-mode cannot be used, use low rpm throttle instead 

        # e2s pin setup 
        self.pin_e2s_top = 16 
        self.pin_e2s_bottom = 20 

        # emergency switch pin setup 
        self.pin_em_sw = 21 

        # encoder pin setup & count, pos
        # these variable are crucial to the mission, so manage these as instance variable of class 
        # (not using as an argument so to manage across method)
        self.count = 0 
        self.pos = 0 
        

        self.actu = selemod.Actuator(pin_esc=self.pin_esc, pin_servo_1=self.pin_servo_1, 
                        freq_esc=self.freq_esc, freq_servo=self.freq_servo, 
                        brakeon_duty=self.brakeon_duty, brakeoff_duty=self.brakeoff_duty, 
                        throttle_a0=self.throttle_a0, throttle_a1=self.throttle_a1) #actuator(DC & servo motor)
        self.e2s = E2S(self.pin_e2s_top, self.pin_e2s_bottom) #E2S
        self.em_sw = EM_SW(self.pin_em_sw) #emergency switch 
        
        if self.bme_is_use: 
            self.bme280 = Bme280(0x76) #bme280 sensor
        if self.sht_is_use: 
            self.sht31 = Sht31(0x45) #sht31 sensor
        
        print('calibrated esc "y" or "n"')
        inp = input()
        if inp == "y": 
            pass 
        elif inp == "n": 
            self.actu.calibrate_esc() #calibrate esc 
        self.actu.brakeoff() #servo brake off b4 climbing 

    def motor(self, e2s_flag, em_flag): 
        """
        Arguments
        -------------------------------------------------------------------
        e2s_flag(tuple) : (top e2s flag, bottom e2s flag)
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

        if self.mode == 0: 
            if self.lower_lim <= self.pos < self.middle_lim1: 
                self.target_throttle = self.throttle1
            elif self.middle_lim1 <= self.pos < self.middle_lim2: 
                self.target_throttle = self.throttle2
            elif self.middle_lim2 <= self.pos < self.upper_lim: 
                self.target_throttle = self.throttle3

            if self.current_throttle != self.target_throttle: #change throttle value only if current throttle and target throttle is different
                self.actu.new_throttle(self.target_throttle)
                self.current_throttle = self.target_throttle
            
            #### esc stop sequence ####
            # if near the goal, stop esc (this area is above safe zone, so immediately set throttle 0 once the climber reach this area)
            if self.upper_lim <= self.pos: 
                print("climber near the goal")
                self.actu.stop_esc(self.current_throttle)
                self.actu.brakeon()
                print("switching to heli-mode")
                # cmd to switch to heli-mode 
                self.mode = 1 

            # E2S emergency stop 
            e2s_0_flag, e2s_1_flag = e2s_flag
            if e2s_0_flag == 0: 
                print("top e2s ON")
                print("turning off actuator")
                self.actu.brakeon()
                self.actu.stop_esc(self.current_throttle)
                self.mode = 1
            elif e2s_1_flag == 0: 
                print("bottom e2s ON")
                print("turning off actuator")
                self.actu.brakeon()
                self.actu.stop_esc(self.current_throttle)
                self.mode = 1
            else: 
                pass 

            # Emergency switch stop 
            if em_flag == 1: 
                print("emergency switch ON")
                print("turning off actuator")
                self.actu.brakeon()
                self.actu.stop_esc(self.current_throttle)
                sys.exit()
            else: 
                pass  

        # once self.mode is set to 1 (climb down), never change self.mode to 0 (for safety reason)
        # while self.mode = 1, continue heli-mode -> change to normal mode and set throttle 0 
        elif self.mode == 1: 
            #swith to heli-mode every 5% of DISTANCE
            if self.current_throttle != self.throttle_const: 
                print("setting throttle 40%")
                self.actu.new_throttle(self.throttle_const)
                self.current_throttle = self.throttle_const

            if int(self.pos)%(self.DISTANCE*self.REDUCE_RATE) == 0: 
                print("turning off motor and activate brake for 5sec")
                self.actu.stop_esc(self.current_throttle)
                self.actu.brakeon()
                sleep(5)
        
    # def brake(self, servo_flag):
    #     """ 
    #     sevo_flag(int) : binary integer flag whether turning on brake or not 
    #     """
    #     if servo_flag==0: 
    #         self.actu.ser_1.brakeon()
    #     elif servo_flag==1: 
    #         self.actu.ser_1.brakeoff() 

    def _e2s(self): 
        e2s_0_flag = self.e2s.read_top()
        e2s_1_flag = self.e2s.read_bottom()
        return (e2s_0_flag, e2s_1_flag)

    
    def _em_sw(self): 
        em_flag = self.em_sw.read()
        return em_flag
    
    def _encoder(self): 
        '''based on encoder count value, compute climber's position'''
        while True: 
            # self.count = ... #update counter value here 
            self.pos = 2 * pi * self.RADIUS * self.count
            print("count: {}    position{}m\n".format(self.count, self.pos))


    def _bme280(self): 
        press, temp, humid = self.bme280.read()
        return (press, temp, humid)

    def _sht31(self): 
        temp, humid = sht31.read()
        return (temp, humid)


    def run(self):
        # this is main program 
        
        # process _encoder function in another thread
        enc_thread = threading.Thread(target=self._encoder)
        enc_thread.start()
        enc_thread.join()

        while True: 
            try: 
                em_flag = self._em_sw()
                e2s_flag = self._e2s()
                # self._encoder()
                self.motor(e2s_flag, em_flag)
            except KeyboardInterrupt: 
                print("Aborting the sequence")
                self.stop_esc(self.current_throttle)
                self.actu.brakeon()
                gpio.cleanup()
                pigpio.stop()
                sys.exit()