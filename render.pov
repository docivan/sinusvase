camera{ location <0,5,-10> look_at <0,5,0> right x*1 }
light_source { <1000,1000,-1000>, rgb <1,1,1> }
light_source { <-10000,-10000,0>, rgb <0.5,0.5,0.5> }
// sphere { <0,5,0>, 2 pigment {color <1,0,0>} }

#declare Vase =
#include "vase.pov"

object {Vase rotate <-90,0,0> scale 0.45 translate <0,1.4,0> pigment{ color <1,1,1> }}
