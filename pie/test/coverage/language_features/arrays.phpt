--TEST--
Test for array creation

--FILE--
<?php
$a = array();
var_dump($a);
$a = array(
    1 => "5",
    6,
    "3" => 4,
    7,
    8
);
var_dump($a);
?>
--EXPECT--
array(0) {
}
array(5) {
  [1]=>
  string(1) "5"
  [2]=>
  int(6)
  [3]=>
  int(4)
  [4]=>
  int(7)
  [5]=>
  int(8)
}