include<includes.scad>

linear_extrude(box_thickness)
difference(){
    {offset(box_thickness)
    top_plate();}
    top_plate();}
    
linear_extrude(box_thickness+2)
difference(){
top_plate();
    union(){
        translate([50,(button_hole+button_gap)*.5,0])
        circle(d=button_hole);
        translate([50,(button_hole+button_gap)*1.5,0])
        circle(d=button_hole);
        translate([50,(button_hole+button_gap)*2.5,0])
        circle(d=button_hole);
        translate([50,(button_hole+button_gap)*3.5,0])
        circle(d=button_hole);
        translate([50,(button_hole+button_gap)*4.5,0])
        circle(d=button_hole);
        translate([85,(button_hole+button_gap)*4.5,0])
        circle(d=led_hole);
        }
}
