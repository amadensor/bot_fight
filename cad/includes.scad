$fn=100;
button_hole=29;
button_gap=10;
led_hole=5.5;
box_height=70;
box_depth=100;
box_thickness=2;
port_height=20;
port_width=15;

button_width=((button_hole+button_gap)*5);
module top_plate(){square([box_depth,button_width]);}

