mpy-cross timer_code/timer_display/microdot/src/microdot/microdot.py
mpy-cross timer_code/timer_display/microdot/src/microdot/utemplate.py
mpy-cross timer_code/timer_display/utemplate/utemplate/compiled.py
mpy-cross timer_code/timer_display/utemplate/utemplate/recompile.py
mpy-cross timer_code/timer_display/utemplate/utemplate/source.py

rshell mkdir /pyboard/templates
rshell mkdir /pyboard/microdot
rshell mkdir /pyboard/utemplate
rshell mkdir /pyboard/lib
rshell cp timer_code/timer_display/* /pyboard
rshell cp timer_code/functions.py /pyboard
rshell cp timer_code/net_config.txt /pyboard
rshell cp timer_code/timer_display/templates/* /pyboard/templates
rshell cp timer_code/timer_display/microdot/src/microdot/microdot.mpy /pyboard/microdot
rshell cp timer_code/timer_display/microdot/src/microdot/utemplate.mpy /pyboard/microdot
rshell cp timer_code/timer_display/utemplate/utemplate/*.mpy /pyboard/utemplate
rshell cp timer_code/timer_display/micropython-tm1637/tm1637.py /pyboard/lib
