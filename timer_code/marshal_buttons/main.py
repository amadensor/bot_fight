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

def start_button(pin):
    global action
    action="start"

def stop_button(pin):
    global action
    action="stop"

def reset_button(pin):
    global action
    action="reset"

def config_button(pin):
    global action
    action="config"

def countdown_button(pin):
    global action
    action="countdown"

start_pin=machine.Pin(start_pin_num,machine.Pin.IN, machine.Pin.PULL_DOWN)
start_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=start_button)

countdown_pin=machine.Pin(countdown_pin_num,machine.Pin.IN, machine.Pin.PULL_DOWN)
countdown_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=countdown_button)

reset_pin=machine.Pin(reset_pin_num,machine.Pin.IN, machine.Pin.PULL_DOWN)
reset_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=reset_button)

config_pin=machine.Pin(config_pin_num,machine.Pin.IN, machine.Pin.PULL_DOWN)
config_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=config_button)

stop_pin=machine.Pin(stop_pin_num,machine.Pin.IN, machine.Pin.PULL_DOWN)
stop_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=stop_button)


def hardware_loop():
    global action
    if action:
        message={"button":action}
        msg_bus.send_message(message)
        time.sleep(.1)
        action=None
    
