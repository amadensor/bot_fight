import functions
import display_driver

msg_bus=functions.Bus()
display=display_driver.Large_display()
connected=False

def display_time(seconds):
    minutes=seconds//60
    remain=seconds%60
    display_val=(minutes*100)+remain
    display.display_number(display_val)
    
def main():
    global connected
    while True:
        if not connected:
            display.display_number(888)
        msg=msg_bus.handler()
        if msg:
            connected=True
            disp_time=msg.get('display_time')
            if disp_time:
                try:
                    display_time(disp_time)
                except:
                    pass
main()
