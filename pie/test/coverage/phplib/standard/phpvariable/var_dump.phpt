--DOC--
Test for var_dump() function.
http://www.php.net/manual/en/function.var_dump.php

TODO: add array and object support
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
float(1.3e+55)
float(1.3e-45)
float(1.1)
float(1.1e+14)
string(3) "yes"
string(1) "1"
multiple parameters test
int(1)
float(1.1)
string(6) "string"
bool(false)
variables test
int(51)
string(3) "yes"
float(42.5)
++++++++++++++++++++++++++++++++++++
array(0) {
}
array(3) {
  [0]=>
  int(1)
  [1]=>
  int(2)
  [2]=>
  int(3)
}
array(2) {
  [3]=>
  float(3.23)
  [4]=>
  int(135)
}
array(3) {
  [0]=>
  int(1)
  [1]=>
  string(6) "string"
  [2]=>
  array(2) {
    [5]=>
    array(0) {
    }
    ["menu"]=>
    string(4) "dish"
  }
}