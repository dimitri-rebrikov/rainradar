$fn=20;

/*
positions of the drilling holes
*/
dhLid1=[5,6.5,0];
dhLid2=[5,36.5,0];
dhLid3=[205,6.5,0];
dhLid4=[205,36.5,0];
dhLed1=[15,11.5,0];
dhLed2=[15,31.5,0];
dhLed3=[138,11.5,0];
dhLed4=[138,31.5,0];
dhEsp1=[153,10,0];
dhEsp2=[153,33,0];
dhEsp3=[200,10,0];
dhEsp4=[200,33,0];

module parts() {
    // just to show all parts necessary
    translate([-10,0,0]) standoff12FF();
    translate([-20,0,0]) standoff06MF();
    translate([-30,0,0]) screw();
    translate([-40,0,0]) screwNut();
    translate([-50,0,0]) washer();
}

module explode_view() {
    // explode view of elements
    casingWithHoles();
    translate([0,0,-10]) bottomScrews();
    translate([0,0,30]) {
        ledStandoffs();
        espStandoffs();
        lidStandoffs1();
    }
    translate([0,0,45]) lidWashers();
    translate([0,0,60]) lidStandoffs2();
    translate([0,0,50]) ledBase();
    translate([0,0,55]) esp();
    translate([0,0,65]) espScrews();
    translate([0,0,60]) ledScrewNuts();
    translate([0,0,70]) ledUnmounted();
    translate([0,0,80]) lid();
    translate([0,0,110]) lidScrews();
}

parts();
explode_view();
// or
// projection for creating a dxf file for casing drillings
//projection(cut=true) translate([0,0, -1])
//    casingWithHoles();
// or
// projection for creating a dxf file for casing side view
//projection(cut=true) translate([0,0, 1]) rotate([0,90,0])
//    casingWithHoles();
// or
// projection for creating a dxf file for lid
//projection(cut=true) translate([0,0, -20])
//    lid();
// or
// projection for creating a dxf file for lid USB side
//projection(cut=true) translate([0,0, 209]) rotate([0,90,0])
//    lid();


module standoff12FF() {
    /*
    standoff m2.5 x 12 mm
    */
    difference(){
        cylinder(d=5,h=12,$fn=6);
        cylinder(d=2.5,h=12,$fn=50);
    }
}

module standoff06MF() {
    /*
    standoff m2.5 x 6 mm + 4 mm
    */
    difference(){
        cylinder(d=5,h=6,$fn=6);
        cylinder(d=2.5,h=5,$fn=50);
    }
    translate([0,0,4]) cylinder(d=2.5,h=6,$fn=50);
}

module screw() {
    /*
    screw m2.5
    */
    difference() {
        cylinder(d=5,h=2,$fn=50);
        translate([-2.5,-0.5,0]) cube([5, 1, 1]);
    }
    translate([0,0,2]) cylinder(d=2.5,h=4,$fn=50);
}

module screwNut() {
    /*
    screw nut m2.5
    */
    difference(){
        cylinder(d=5,h=2,$fn=6);
        cylinder(d=2.5,h=2,$fn=50);
    }
}

module washer() {
    /*
    washer m2.5 x 1 mm
    */
    difference(){
        cylinder(d=5,h=1,$fn=50);
        cylinder(d=2.5,h=1,$fn=50);
    }
}

module drillingHole() {
    cylinder(d=3,h=3,$fn=50);
}

module casing() {
    cube([210,43,1.5]);
    cube([210,1.5,22.5]);
    translate([0,41.5,0]) cube([210,1.5,22.5]);
}

module repeatForPositions(positions) {
    for( position = positions ) {
        translate(position) children();
    }
}

module repeatForLidDrillingHoles() {
    repeatForPositions([dhLid1,dhLid2,dhLid3,dhLid4]) 
        children();
}

module repeatForLedDrillingHoles() {
    repeatForPositions([dhLed1,dhLed2,dhLed3,dhLed4]) 
        children();
}

module repeatForEspDrillingHoles() {
    repeatForPositions([dhEsp1,dhEsp2,dhEsp3,dhEsp4]) 
        children();
}

module casingWithHoles() {
    difference() {
        casing();
        repeatForLidDrillingHoles() 
            drillingHole();
        repeatForLedDrillingHoles() 
            drillingHole();
        repeatForEspDrillingHoles() 
            drillingHole();
    }
}

module bottomScrews() {
    repeatForLidDrillingHoles() 
        screw();
    repeatForLedDrillingHoles() 
        screw();
    repeatForEspDrillingHoles() 
        screw();
}

module lidWashers() {
    repeatForLidDrillingHoles() 
        washer();
}

module ledStandoffs() {
    repeatForLedDrillingHoles()
        standoff06MF();
}

module espStandoffs() {
    repeatForEspDrillingHoles()
        standoff12FF();
}

module lidStandoffs1() {
    repeatForLidDrillingHoles()
        standoff12FF();
}

module lidStandoffs2() {
    repeatForLidDrillingHoles()
        rotate([180,0,0])
            standoff06MF();
}

module esp() {
    difference() {
        translate(dhEsp1) {
            translate([-2.5, -2.5, 0]) {
                cube([52,28,1]);
                translate([7,6,1]) cube([18,16,2]);
                translate([47,9,0]) cube([5,10,3]);
            }
        }
        repeatForEspDrillingHoles() 
            drillingHole();
    }
    
}

module espScrews() {
    repeatForEspDrillingHoles()
        rotate([180,0,0])
            screw();
}   

module ledBase() {
     difference() {
        translate(dhLed1) {
            translate([-2.5, -6, 0]) {
                cube([128,32,1]);
                translate([123,11,-3]) cube([10,10,3]);
                translate([6,5,1]) cube([116,22,5]);
                translate([32,0,5]) cube([64,32,7]);
            }
        }
        repeatForLedDrillingHoles() 
            drillingHole();
    }
}

module ledScrewNuts() {
    repeatForLedDrillingHoles()
        screwNut();
}   

module ledUnmounted() {
    translate(dhLed1) {
        translate([-2.5, -6, 0]) {
            cube([32,32,7]);
            translate([32*3,0,0]) cube([32,32,7]);
        }
    }
}

module lidTop() {
   difference() {
        cube([210,40,3]);
        translate([0,-1.5,0]) repeatForLidDrillingHoles() 
            drillingHole();
        translate([200,28,0])
            drillingHole();
   }
}

module lidSide() {
    cube([3,40,19]);
}

module lidSideUsb() {
    difference() {
        lidSide();
        translate([0,12.5,9]) cube([3,15,10]);
    }
}

module lid() {
    translate([0,1.5,0]) {
        translate([0,0,19]) lidTop();
        lidSide();
        translate([207,0,0]) lidSideUsb();
    }
}

module lidScrews() {
    repeatForLidDrillingHoles()
        rotate([180,0,0])
            screw();
}     

    


