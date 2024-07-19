import time
import tm1637
import functions

msg_bus=functions.Bus()
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
    first_time=True
    while True:
        if not connected and first_time:
            first_time=False
            display.show('Connect')
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
                if len(str(disp_value))>4:
                    try:
                        display.scroll(disp_value)
                    except:
                        pass
                else:
                    try:
                        display.show(str(disp_value)+"    ")
                    except:
                        pass

main()
