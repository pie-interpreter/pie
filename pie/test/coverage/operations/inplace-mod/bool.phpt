--TEST--
Test in-place for bool
--FILE--
<?php
$a = true;
$a %= true;
echo $a;
?>
--EXPECT--
0