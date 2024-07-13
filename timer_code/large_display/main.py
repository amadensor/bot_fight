import time
import tm1637
import functions

msg_bus=functions.Bus()
latch=machine.Pin(19,machine.Pin.OUT)
display=tm1637.TM1637(clk=machine.Pin(20),dio=machine.Pin(21))
connected=False

def display_time(seconds):
    minutes=int(seconds/60)
    remain=seconds%60
    display_val=(minutes*100)+remain
    display_str='    '+str(display_val)
    display.show(display_str[-4:],colon=True)
    
def main():
    global connected
    while True:
        latch.off()
        if not connected:
            display.show('conn')
            latch.on()
            time.sleep_us(tm1637.TM1637_DELAY)
        msg=msg_bus.handler()
        if msg:
            connected=True
            disp_time=msg.get('display_time')
            disp_value=msg.get('display_value')
            if disp_time:
                try:
                    display_time(disp_time)
                except:
                    pass
            if disp_value:
                display.show(str(disp_value)+"    ")
            latch.on()
            time.sleep_us(tm1637.TM1637_DELAY)

main()
