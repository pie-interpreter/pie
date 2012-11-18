--TEST--
Test in-place for int numbers
--FILE--
<?php
$a = 5;
$a -= 10;
echo $a;
?>
--EXPECT--
-5