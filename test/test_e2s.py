import RPi.GPIO as gpio
import time
from selemod import E2S

#このプログラムの起動は時限式にする
# もしくは、クライマーの高度が上端のダンパー付近に来た時に、起動する

# GPIO.setmode(GPIO.BCM)

pin_e2s_top = 16 
pin_e2s_bottom = 20

e2s_ = E2S(pin_e2s_top, pin_e2s_bottom)
print("instantiation cuccessed!")
top_sw_state = e2s_.read_top
print(top_sw_state)