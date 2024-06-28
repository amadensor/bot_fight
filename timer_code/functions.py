import json
import tm1637
import machine
import collections
import time

display=tm1637.TM1637(clk=machine.Pin(3),dio=machine.Pin(2))

def display_time(seconds):
    minutes=int(seconds/60)
    remain=seconds%60
    display_val=(minutes*100)+remain
    display_number(display_val)


def display_number(disp_number):
    display_patterns=[63,6,91,79,102,109,125,7,127,111]
    display_array=[]
    #Build an array of the digits
    while disp_number:
        display_char=disp_number%10
        disp_number=int(disp_number/10)
        #Use the bit pattern for the shape of the letter
        display_array.append(display_patterns[display_char])
    #Pad with blanks
    while len(display_array)<4:
        display_array.append(0)
    display_array.reverse()
    display_array[1]=display_array[1]+128 # turn on the colon
    display.write(display_array)
    

class Bus:
    def __init__(self):
        self.q=collections.deque((),100)
        self.ser0=machine.UART(0)
        self.ser1=machine.UART(1)

    def send_message(self,msg):
        try:
            msg_txt=json.dumps(msg)+"\n"
            print(msg_txt)
            self.ser1.write(msg_txt)
            self.ser0.write(msg_txt)
        except:
            pass

    def handler(self):
        if self.ser0.any():
            time.sleep(.1)
            msg=self.ser0.readline()
            print("0",msg)
            self.ser1.write(msg)
            try:
                print("queue 0")
                self.q.append(json.loads(msg))
            except:
                pass
        if self.ser1.any():
            time.sleep(.1)
            msg=self.ser1.readline()
            print("1",msg)
            self.ser0.write(msg)
            try:
                print("queue 1")
                self.q.append(json.loads(msg))
            except:
                pass
        if self.q:
            print("ret q")
            return self.q.popleft()
        else:
            return None
