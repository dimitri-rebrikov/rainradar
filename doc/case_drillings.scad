module body() {
    square(size = [205, 43], center=false);
}

module screw_hole() {
    circle(d=3, $fn=50, center=true);
}

module sp32_screw_holes() {
    screw_hole();
    translate([0, 23])
        screw_hole();
    translate([47, 0])
        screw_hole();
    translate([47, 23])
        screw_hole();
}

module led_matrix_screw_holes() {
    screw_hole();
    translate([0, 20])
        screw_hole();
    translate([123, 0])
        screw_hole();
    translate([123, 20])
        screw_hole();
}
    

module all() {
    difference() {
        body();
        translate([6, 10])
            sp32_screw_holes();
        translate([68, 11.5])
            led_matrix_screw_holes();
        translate([10, 4])
            screw_hole();
        translate([10, 39])
            screw_hole();
        translate([195, 4])
            screw_hole();
        translate([195, 39])
            screw_hole();
    }
}

all();