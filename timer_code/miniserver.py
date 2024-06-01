import time
import asyncio
import functions
import json
from microdot.microdot import Microdot,Response
from microdot.utemplate import Template

functions.start_network()

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
    return Template('index.html').render()

@app.route('/timers',methods=['GET'])
async def timer_list(request):
    timers=timer_config.get('timers')
    Response.default_content_type = 'text/html'
    return (str(Template("timer_list.html").render(timers=timers)))

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
    Response.default_content_type = 'text/html'
    return (str(Template("index.html").render()))
@app.get('/start')
async def start(request):
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

@app.get('/stop')
async def stop(request):
    run_timer.stop_time=time.ticks_ms()
    run_timer.mode='stop'
@app.get('/reset')
async def reset(request):
    if run_timer.mode=='countdown':
        run_timer.mode='run'
    if run_timer.mode=='pause':
        run_timer.stop_time=0
        run_timer.elapsed=0
        run_timer.mode='stop'
@app.get('/config')
async def config(request):
    run_timer.config=run_timer.config + 1
    if run_timer.config > (len(timer_config.get('timers'))-1):
        run_timer.config=0
    print(timer_config.get('timers',[])[run_timer.config].get('config_name'))
    display_time(run_timer.config)
@app.get('/countdown')
async def countdown(request):
    run_timer.countdown_start=time.ticks_ms()
    run_timer.hold_mode=run_timer.mode
    run_timer.mode='countdown'

def display_time(seconds):
    minutes=int(seconds/60)
    remain=seconds%60
    display_seconds=("00"+str(remain))[-2:]
    print(str(minutes)+":"+str(display_seconds))


async def main():
    hw_loop=asyncio.create_task( hardware_loop())
    web=asyncio.create_task( app.start_server(port=80, debug=True))
    await hw_loop
    await web

async def hardware_loop():
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

        if run_timer.mode=='countdown':
            if new_countdown_seconds != countdown_seconds:
                countdown_seconds=new_countdown_seconds
                display_time(countdown_duration-countdown_seconds)
        else:
            if new_seconds != seconds:
                seconds=new_seconds
                display_time(timer_duration-seconds)
        
        await asyncio.sleep(.1)

asyncio.run(main())

