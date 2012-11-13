--TEST--
Test in-place for bool
--FILE--
<?php
$a = true;
$a *= true;
echo $a;
echo "=\n";
$a *= false;
echo $a . "=";
?>
--EXPECT--
1=
0=