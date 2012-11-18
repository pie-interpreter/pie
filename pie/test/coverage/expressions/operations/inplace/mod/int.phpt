--TEST--
Test in-place for int numbers
--FILE--
<?php
$a = 5;
$a %= 3;
echo $a;
?>
--EXPECT--
2