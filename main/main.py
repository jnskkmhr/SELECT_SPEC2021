from mission import Resilience
import selemod 
import RPi.GPIO as gpio 
import pigpio 
import sys 
import time 

def main(): 
    distance = 100 # in meter  
    reduce_rate = 0.05
    spec = {"radius": 0.3, "height": 2} # in meter
    sensor = {"bme" : False, "sht" : False, "counter" : True}
    res = Resilience(distance, reduce_rate, spec, sensor)
    res.run()

if __name__ == "__main__": 
    main()