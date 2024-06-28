mpy-cross timer_code/core_processor/microdot/src/microdot/microdot.py
mpy-cross timer_code/core_processor/microdot/src/microdot/utemplate.py
mpy-cross timer_code/core_processor/utemplate/utemplate/compiled.py
mpy-cross timer_code/core_processor/utemplate/utemplate/recompile.py
mpy-cross timer_code/core_processor/utemplate/utemplate/source.py

rshell mkdir /pyboard/templates
rshell mkdir /pyboard/microdot
rshell mkdir /pyboard/utemplate
rshell mkdir /pyboard/lib
rshell cp timer_code/core_processor/* /pyboard
rshell cp timer_code/functions.py /pyboard
rshell cp timer_code/net_config.txt /pyboard
rshell cp timer_code/core_processor/templates/* /pyboard/templates
rshell cp timer_code/core_processor/microdot/src/microdot/microdot.mpy /pyboard/microdot
rshell cp timer_code/core_processor/microdot/src/microdot/utemplate.mpy /pyboard/microdot
rshell cp timer_code/core_processor/utemplate/utemplate/*.mpy /pyboard/utemplate
rshell cp timer_code/core_processor/micropython-tm1637/tm1637.py /pyboard/lib
