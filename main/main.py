from mission import Resilience
import selemod 
import RPi.gpio as gpio 
import pigpio 
import sys 
import time 

def main(): 
    distance = 100 
    spec = {"radius": 0.3, "height": 2}
    res = Resilience(distance, spec)
    res.run()