--FILE--
<?php
var_dump(false);
var_dump(true);
var_dump(null);
var_dump(-1);
var_dump(1);
var_dump(43423);
var_dump(1.1);
var_dump(1.3123);
var_dump(-1.32);
var_dump(1.3e55);
var_dump(1.3e-45);
var_dump(1.10);
//var_dump(1.1e13); FIXME: this should be uncommented
var_dump(1.1e14);
var_dump("yes");
var_dump("1")
?>
--EXPECT--
bool(false)
bool(true)
NULL
int(-1)
int(1)
int(43423)
float(1.1)
float(1.3123)
float(-1.32)
float(1.3E+55)
float(1.3E-45)
float(1.1)
float(1.1E+14)
string(3) "yes"
string(1) "1"