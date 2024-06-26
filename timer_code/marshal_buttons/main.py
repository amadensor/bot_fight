import time
import functions
import machine

start_pin_num=15
countdown_pin_num=14
reset_pin_num=13
config_pin_num=12
stop_pin_num=11
ready_light=machine.Pin(machine.Pin(10),machine.Pin.OUT)

action=None
msg_bus=functions.Bus()

ready_light.on()

start_pin=machine.Pin(start_pin_num,machine.Pin.IN, machine.Pin.PULL_DOWN)
countdown_pin=machine.Pin(countdown_pin_num,machine.Pin.IN, machine.Pin.PULL_DOWN)
reset_pin=machine.Pin(reset_pin_num,machine.Pin.IN, machine.Pin.PULL_DOWN)
config_pin=machine.Pin(config_pin_num,machine.Pin.IN, machine.Pin.PULL_DOWN)
stop_pin=machine.Pin(stop_pin_num,machine.Pin.IN, machine.Pin.PULL_DOWN)

def hardware_loop():
    global action
    if start_pin.value():
        action="start"
    if countdown_pin.value():
        action="countdown"
    if reset_pin.value():
        action="reset"
    if config_pin.value():
        action="config"
    if stop_pin.value():
        action="stop"
    if action:
        message={"button":action}
        msg_bus.send_message(message)
        time.sleep(.25)
        action=None
    
while True:
    hardware_loop()