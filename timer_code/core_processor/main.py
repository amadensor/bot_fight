import time
import asyncio
import network
import functions
import json
from microdot.microdot import Microdot,Response,redirect
from microdot.utemplate import Template

ready_light=machine.Pin(machine.Pin(10),machine.Pin.OUT)

action=None

msg_bus=functions.Bus()
msg_bus.send_message({"display_time":0})

def start_network():
    with open("net_config.txt","r") as net_data:
        config_string=net_data.read()
        net_config_data=json.loads(config_string)
    ap_if = network.WLAN(network.AP_IF)
    print(net_config_data)
    ap_if.config(ssid=net_config_data.get('ssid'),key=net_config_data.get('psk')) # Connect to an AP
    if net_config_data.get('ifc'):
        ap_if.ifconfig(net_config_data.get('ifc'))
    ap_if.active(True)
    while not ap_if.active():
        print(ap_if.active())
    print(ap_if.isconnected())
    print(ap_if.ifconfig())
    return ap_if


ap_if=start_network()

while not ap_if.isconnected():
    print(ap_if.isconnected())
    time.sleep(1)

for t in range(3):
    ip=ap_if.ifconfig()[0].split('.')
    for digit in ip:
        msg_bus.send_message({"display_value":(int(digit))})
        time.sleep(.5)
    msg_bus.send_message({"display_value":"    "})
    time.sleep(.25)
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

app=Microdot()

@app.route('/')
async def index(request):
    Response.default_content_type = 'text/html'
    return Template('index.html').render(timer=timer_config.get('timers')[run_timer.config])

@app.route('/timers',methods=['GET'])
async def timer_list(request):
    timers=timer_config.get('timers')
    Response.default_content_type = 'text/html'
    return (str(Template("timer_list.html").render(timers=timers)))

@app.route('/timers/add',methods=['GET'])
async def timer_add(request):
    timer_config['timers'].append(
        {
            "box_lights": False,
            "time_limit_minutes": 3,
            "pits_time_minutes": 0,
            "time_limit_seconds": 0,
            "countdown_duration": 10,
            "pits_active": False,
            "pits_time_seconds": 0,
            "config_name": "New Config",
            "competitor_controls": False
            }
        )
    return redirect('/timers')

@app.route('/timers/delete/<id>',methods=['GET'])
async def timer_add(request,id):
    timer_config['timers'].pop(int(id))
    return redirect('/timers')

@app.route('/timers',methods=['POST'])
async def timer_list(request):
    global timer_config
    form_data=request.form
    rows=len(form_data.getlist('time_limit_minutes'))
    new_config=[]
    for t in range(rows):
        new_config.append(
            {
                'time_limit_minutes':int(form_data.getlist('time_limit_minutes')[t]),
                'box_lights':(form_data.getlist('box_lights')[t]=='True'),
                'pits_time_minutes':int(form_data.getlist('pits_time_minutes')[t]),
                'time_limit_seconds':int(form_data.getlist('time_limit_seconds')[t]),
                'countdown_duration':int(form_data.getlist('countdown_duration')[t]),
                'pits_active':(form_data.getlist('pits_active')[t]=='True'),
                'pits_time_seconds':int(form_data.getlist('pits_time_seconds')[t]),
                'config_name':form_data.getlist('config_name')[t],
                'competitor_controls':form_data.getlist('competitor_controls')[t]=='True',
        }   
        )
    timer_config['timers']=new_config

    with open("timer_config.txt","w") as timer_file:
        timer_file.write(json.dumps(timer_config))
    return redirect('/timers')

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

async def main():
    print("web")
    web=asyncio.create_task( app.start_server(port=80, debug=True))
    print("hw")
    #hw_loop=asyncio.create_task( hardware_loop())
    await hardware_loop()
    print("wait")
    await web

async def hardware_loop():
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
            await asyncio.sleep(.5)
            print("next")
            action=None
        await asyncio.sleep(0)

asyncio.run(main())


