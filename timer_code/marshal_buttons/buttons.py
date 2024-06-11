import functions
import machine
import requests
import json
import time
start_pin_num=15
countdown_pin_num=14
reset_pin_num=13
config_pin_num=12
stop_pin_num=11
action=None

with open("marshal_config.txt","r") as net_data:
    config_string=net_data.read()
    config_data=json.loads(config_string)

sta_if=functions.start_network()

if not config_data.get('timer_url'):
    ip=sta_if.ifconfig[0].split(',')
    url="http://"+ip[0]+'.'+ip[1]+'.'+ip[2]+'.1'
    config_data['timer_url']=url

while not sta_if.isconnected():
    print(sta_if.isconnected())
    time.sleep(1)
print(sta_if.ifconfig())

def start_button(pin):
    action="start"
    print("start pressed")

def countdown_button(pin):
    action="countdown"
    print("countdown pressed")

def reset_button(pin):
    action="reset"
    print("reset pressed")

def config_button(pin):
    action="config"
    print("config pressed")

def stop_button(pin):
    action="stop"
    print("stop pressed")


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


def main():
    global action
    if (action):
        url=config_data.get('timer_url')+"/"+action
        print(action+" sent", url)
        requests.get(url)
        print('responded')
        time.sleep(.5)
        action=None
    time.sleep(.01)

while True:
    main()
