import asyncio
import functions
import json
from microdot.microdot import Microdot,Response
from microdot.utemplate import Template

functions.start_network()

with open("timer_config.txt","r") as timer_data:
    timer_string=timer_data.read()
    timer_config=json.loads(timer_string)

app=Microdot()

@app.route('/')
async def index(request):
    print(json.dumps(request.args))
    print(json.dumps(request.json))
    return('Hello World')

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

async def main():
    await app.start_server(port=80)

asyncio.run(main())