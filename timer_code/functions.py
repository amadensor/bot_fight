import network
import json

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
