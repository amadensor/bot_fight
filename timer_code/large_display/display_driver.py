import time
import machine

class Large_display:
    def __init__(self, latch=19, clock=20, serial=21, delay=1000):
        self.latch=machine.Pin(latch,machine.Pin.OUT)
        self.clock=machine.Pin(clock, machine.Pin.OUT)
        self.serial=machine.Pin(serial,machine.Pin.OUT)
        self.delay=delay
        a=1<<0 
        c=1<<5
        b=1<<6
        d=1<<4
        e=1<<3
        f=1<<1
        g=1<<2
        dp=1<<7
        self.patterns=[
            a + b + c + d + e + f,
            b + c,
            a + b + d + e + g,
            a + b + c + d + g,
            f + g + b + c,
            a + f + g + c + d,
            a + f + g + e + c + d,
            a + b + c,
            a + b + c + d + e + f + g,
            a + b + c + d + f + g
        ]

    def display_number(self,display_number):
        self.clock.off()
        self.latch.off()
        display_bytes=[]
        while display_number:
            display_digit=display_number%10
            display_number=display_number//10
            display_bytes.append(self.patterns[display_digit])
        while (len(display_bytes) < 4):
            display_bytes.append(0)
        for i in range(4):
            byte=display_bytes[i]
            for t in range(8):
                bit=byte & 1 << (7-t)
                self.clock.off()
                time.sleep_us(self.delay)
                if bit:
                    self.serial.on()
                else:
                    self.serial.off()
                time.sleep_us(self.delay)
                self.clock.on()
                time.sleep_us(self.delay)
        self.latch.off()
        time.sleep_us(self.delay)
        self.latch.on()
        time.sleep_us(self.delay)

