from mission import Resilience
import selemod 
import RPi.gpio as gpio 
import pigpio 
import sys 
import time 

def main(): 
    distance = 100 # in meter  
    spec = {"radius": 0.3, "height": 2} # in meter
    res = Resilience(distance, spec)
    res.run()

if __name__ == "__main__": 
    main()