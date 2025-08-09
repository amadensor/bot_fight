import time
import functions
import json

ready_light=machine.Pin(machine.Pin(10),machine.Pin.OUT)

action=None

msg_bus=functions.Bus()
msg_bus.send_message({"display_time":0})

msg_bus.send_message({"display_value":"ready"})

ready_light.on()

class BotTimer():
    start_time=0
    stop_time=0
    mode='stop'
    hold_mode='run'
    config=0
    countdown_start=0
    elapsed=0

run_timer=BotTimer()

with open("timer_config.txt","r") as timer_data:
    timer_string=timer_data.read()
    timer_config=json.loads(timer_string)

def start():
    #print("start")
    if run_timer.mode=='pause':
        run_timer.start_time=time.ticks_ms()-run_timer.elapsed
        run_timer.mode='run'
    else:
        if run_timer.mode=='run':
            run_timer.elapsed=time.ticks_ms()-run_timer.start_time
            run_timer.mode='pause'
    if run_timer.mode=='stop':
        run_timer.start_time=time.ticks_ms()
        run_timer.mode='run'

def stop():
    #print("stop")
    run_timer.stop_time=time.ticks_ms()
    run_timer.mode='stop'

def reset():
    #print("reset")
    if run_timer.mode=='countdown':
        run_timer.mode='run'
    if run_timer.mode=='pause':
        run_timer.stop_time=0
        run_timer.elapsed=0
        run_timer.mode='stop'

def config_handler():
    #print("config")
    run_timer.config=run_timer.config + 1
    if run_timer.config > (len(timer_config.get('timers'))-1):
        run_timer.config=0
    print(timer_config.get('timers',[])[run_timer.config].get('config_name'))
    msg_bus.send_message({"display_time":(run_timer.config)+1})

def countdown():
    #print("countdown")
    run_timer.countdown_start=time.ticks_ms()
    if run_timer.mode !="countdown":
        run_timer.hold_mode=run_timer.mode
    run_timer.mode='countdown'

def main():
    hardware_loop()

def hardware_loop():
    print("hw loop")
    global action
    seconds=1
    new_seconds=0
    countdown_seconds=0
    new_countdown_seconds=0
    while True:
        config=timer_config.get('timers')[run_timer.config]
        timer_duration=(config.get('time_limit_minutes')*60)+config.get('time_limit_seconds')
        countdown_duration=config.get('countdown_duration')
        if run_timer.mode=='stop':
            new_seconds=0
        #if run_timer.mode=='pause':
        #    new_seconds=timer_duration-int(run_timer.elapsed/1000)
        if run_timer.mode=='run':
            new_seconds=int((time.ticks_ms()-run_timer.start_time)/1000)
            if seconds >= timer_duration:
                run_timer.mode='stop'
        if run_timer.mode=='countdown':
            new_countdown_seconds=int((time.ticks_ms()-run_timer.countdown_start)/1000)
        if run_timer.mode=='countdown' and (new_countdown_seconds >= countdown_duration):
            run_timer.countdown_start=0
            run_timer.mode=run_timer.hold_mode
            #run_timer.mode='run'

        if run_timer.mode=='countdown':
            if new_countdown_seconds != countdown_seconds:
                countdown_seconds=new_countdown_seconds
                msg_bus.send_message({"display_time":(countdown_duration-countdown_seconds)})
        else:
            if new_seconds != seconds:
                seconds=new_seconds
                msg_bus.send_message({"display_time":(timer_duration-seconds)})
        
        msg=msg_bus.handler()
        if msg:
            action=msg.get('button')

        if action:
            if action=="start":
                start()
            if action=="stop":
                if run_timer.mode=="stop":
                    print("double stop")
                    app.shutdown()
                    ready_light.off()
                    machine.reset()
                    break
                stop()
            if action=="reset":
                reset()
            if action=="config":
                config_handler()
            if action=="countdown":
                countdown()
            print("do")
            print("next")
            action=None

main()


