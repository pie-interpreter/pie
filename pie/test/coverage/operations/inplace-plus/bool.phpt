--TEST--
Test in-place for bool
--FILE--
<?php
$a = false;
$a += true;
echo $a;
echo "=\n";
$a += false;
echo $a . "=";
?>
--EXPECT--
1=
1=