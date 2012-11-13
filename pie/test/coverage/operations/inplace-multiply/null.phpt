--TEST--
Test in-place for null
--FILE--
<?php
$a = null;
$a *= null;
echo $a;
?>
--EXPECT--
0