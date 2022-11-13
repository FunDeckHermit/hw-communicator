from machine import Pin
from statemachine import LinearStateMachine, TimeBasedStateMachine
from pins import Pins
import time

proj_pins = Pins()
ledlist = proj_pins.get_output_led_list()

btn_sm = LinearStateMachine(n_states=10)
sel_sm = TimeBasedStateMachine(n_states=2)
interrupt_flag = 0
lastclick_time = 0
selected = 0
loop_count = 0

def check_choice():
    global btn_sm, selected
    if ledlist[btn_sm.index] is not proj_pins.led0_inbuilt:
        selected = btn_sm.index
        btn_sm.reset()
        result = True
        
    
def next_selection():
    global btn_sm, sel_sm
    if sel_sm.index is 0:
        sel_sm.next_state()
        btn_sm.next_state()
  
  
def debounce(pin):
    global lastclick_time
    if (time.ticks_ms()-lastclick_time) > 42:
        lastclick_time=time.ticks_ms()
        next_selection()


def increment_loopcount():
    global loop_count
    loop_count = loop_count + 1
     

def toggle_status():
    global loop_count
    proj_pins.led_status.value(loop_count % 50 == 0)


def update_leds():
    global btn_sm, sel_sm
    if sel_sm.index == 0:
        proj_pins.exclusive_on(btn_sm.index)
    elif sel_sm.index == 1:
        blink_selected()
    else:
        proj_pins.all_leds_off()
    
def blink_selected():
    global loop_count
    if(loop_count % 6 == 0):
        proj_pins.exclusive_on(selected)
    elif(loop_count % 3 == 0):
        proj_pins.all_leds_off()
        

proj_pins.big_button.irq(trigger=Pin.IRQ_FALLING, handler=debounce)
sel_sm.setwaitcallback(state_index=0, waittime=1000, callback=check_choice)
sel_sm.setwaittime(state_index=1, waittime=2000, auto=True)
while True:
    time.sleep(0.042)
    increment_loopcount()
    toggle_status()
    update_leds()
    
    
