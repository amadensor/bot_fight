import network
import json
import tm1637
import machine

display=tm1637.TM1637(clk=machine.Pin(5),dio=machine.Pin(4))

def start_network():
    with open("net_config.txt","r") as net_data:
        config_string=net_data.read()
        net_config_data=json.loads(config_string)
    sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
    sta_if.scan()                             # Scan for available access points
    sta_if.connect(net_config_data.get('ssid'),net_config_data.get('psk')) # Connect to an AP
    print(sta_if.isconnected())
    sta_if.ifconfig(net_config_data.get('ifc'))
    print(sta_if.ifconfig())

def display_time(seconds):
    display_patterns=[63,6,91,79,102,109,125,7,127,111]
    minutes=int(seconds/60)
    remain=seconds%60
    display_val=(minutes*100)+remain
    display_array=[]
    #Build an array of the digits
    while display_val:
        display_char=display_val%10
        display_val=int(display_val/10)
        #Use the bit pattern for the shape of the letter
        display_array.append(display_patterns[display_char])
    #Pad with blanks
    while len(display_array)<4:
        display_array.append(0)
    display_array.reverse()
    display_array[1]=display_array[1]+128 # turn on the colon
    display.write(display_array)

