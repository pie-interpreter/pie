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
var_dump("1");
//multiple parameters test
echo "multiple parameters test\n";
var_dump(1, 1.1, "string", false);
echo "variables test\n";
$a = 51;
$b = "yes";
$c = 42.5;
var_dump($a, $b, $c);
// arrays
echo "++++++++++++++++++++++++++++++++++++\n";
var_dump(array());
var_dump(array(1,2,3));
var_dump(array("3" => 3.23, 4 => 135));
var_dump(array(1,"string", array(5 => array(), "menu" => "dish")));
?>