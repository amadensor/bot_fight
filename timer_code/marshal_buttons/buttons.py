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
ready_light=machine.Pin(machine.Pin(10),machine.Pin.OUT)

with open("marshal_config.txt","r") as net_data:
    config_string=net_data.read()
    config_data=json.loads(config_string)

sta_if=functions.start_network()

while not sta_if.isconnected():
    print(sta_if.isconnected())
    time.sleep(1)
print(sta_if.ifconfig())

if not config_data.get('timer_url'):
    ip=sta_if.ifconfig()[0].split('.')
    url="http://"+ip[0]+'.'+ip[1]+'.'+ip[2]+'.1'
    config_data['timer_url']=url
ready_light.on()

def start_button(pin):
    global action
    action="start"
    print("start pressed")

def countdown_button(pin):
    global action
    action="countdown"
    print("countdown pressed")

def reset_button(pin):
    global action
    action="reset"
    print("reset pressed")

def config_button(pin):
    global action
    action="config"
    print("config pressed")

def stop_button(pin):
    global action
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
        try:
            requests.get(url, timeout=1)
            print('responded')
            time.sleep(.5)
            action=None
            ready_light.on()
        except:
            ready_light.off()
            print("retry")
    time.sleep(.01)

while True:
    main()

