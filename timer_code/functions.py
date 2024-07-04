import json
import machine
import collections

class Bus:
    def __init__(self):
        self.q=collections.deque((),100)
        self.ser0=machine.UART(0,timeout=2000,timeout_char=100)
        self.ser1=machine.UART(1,timeout=2000,timeout_char=100)

    def send_message(self,msg):
        try:
            msg_txt=json.dumps(msg)+"\n"
            #print(msg_txt)
            self.ser1.write(msg_txt)
            self.ser0.write(msg_txt)
        except:
            pass

    def handler(self):
        while self.ser0.any():
            msg=self.ser0.readline().decode()
            print("0",msg)
            self.ser1.write(msg)
            try:
                print("queue 0")
                self.q.append(json.loads(msg))
            except:
                pass
        while self.ser1.any():
            msg=self.ser1.readline().decode()
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

