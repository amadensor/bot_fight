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
    config=0
    countdown_start=0

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
    print(timers)
    Response.default_content_type = 'text/html'
    return (str(Template("timer_list.html").render(timers=timers)))

@app.route('/timers',methods=['POST'])
async def timer_list(request):
    #timer_config={'timers':request.json}
    timers=timer_config.get('timers')
    test=request.form
    print("Incoming Update")
    print(test)
    #with open("timer_config.txt","w") as timer_file:
    #    timer_file.write(json.dumps(timer_config))
    Response.default_content_type = 'text/html'
    return (str(Template("timer_list.html").render(timers=timers)))
@app.get('/start')
async def start(request):
    run_timer.start_time=time.ticks_ms()
    run_timer.stop_time=0
    run_timer.mode='run'
@app.get('/stop')
async def stop(request):
    run_timer.stop_time=time.ticks_ms()
    run_timer.mode='stop'
@app.get('/reset')
async def reset(request):
    run_timer.stop_time=0
    run_timer.mode='stop'
@app.get('/config')
async def config(request):
    run_timer.config=run_timer.config + 1
    if run_timer.config > (timer_config.get('timers')-1):
        run_timer.config=0
@app.get('/countdown')
async def countdown(request):
    run_timer.countdown_start=time.ticks_ms()
    run_timer.mode='countdown'



async def main():
    hw_loop=asyncio.create_task( hardware_loop())
    web=asyncio.create_task( app.start_server(port=80, debug=True))
    await hw_loop
    await web

async def hardware_loop():
    seconds=0
    new_seconds=0
    countdown_seconds=0
    new_countdown_seconds=0
    while True:
        config=timer_config.get('timers')[run_timer.config]
        if run_timer.mode=='run':
            new_seconds=int((time.ticks_ms()-run_timer.start_time)/1000)
            if new_seconds != seconds:
                seconds=new_seconds
                print(seconds)
        if run_timer.mode=='countdown':
            new_countdown_seconds=int((time.ticks_ms()-run_timer.countdown_start)/1000)
            if new_countdown_seconds != countdown_seconds:
                countdown_seconds=new_countdown_seconds
                print(countdown_seconds)
        if run_timer.mode=='countdown' and (new_countdown_seconds>config.get('countdown_duration')):
            run_timer.countdown_start=0
            run_timer.mode='run'
        await asyncio.sleep(.1)

asyncio.run(main())

