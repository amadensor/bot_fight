#  How to use the system:

*  The network name and password are in the [timer_code/core_processor/net_config.txt] file.
*  The IP address to point your browser to is displayed as the system boots, assuming a display is attached.
*  The web connection is http, not https.
*  Changes to configuration can be done by editing the [timer_code/core_processor/timer_config.txt] configuration file, or by using the web interface.
*  The changes made via web also are saved and will persist after a power cycle.
*  Each cable must connect an A outlet to a B outlet.
   *  This is to accomodate the TX/RX crossover
*  There should be 1 A port and 1 B port left disconnected when complete.
   *  This is because all messages are forwarded, and it would create an infinite loop.
*  The order of modules is gererally unimportant, but the 5VDC should only be injected at one point.
*  The core processor is a Pi Pico W.   All other modules can be normal Pico microcontrollers.

#  Technical details

*  Each module has a Pi Pico in it.  The wiring details are in the [pin_connection.html] file.
*  The entire system runs on a message bususing UART over CAT-5.
*  This is using the microdot and utemplate frameworks for simpler web serving and easier maintenance.
*  As this is all Micropython, very little effort would be required (changing pin numbers) to port this to other microcontrollers.
