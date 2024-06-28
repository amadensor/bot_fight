import functions
import time

msg_bus=functions.Bus()

def main():
    msg=msg_bus.handle()
    if msg:
        print(msg)
    else:
        time.sleep(1)

while True:
    main()