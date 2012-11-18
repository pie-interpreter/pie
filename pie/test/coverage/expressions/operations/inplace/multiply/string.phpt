--TEST--
Test in-place for strings
--FILE--
<?php
$a = "5.5";
$a *= "10";
echo $a;
?>
--EXPECT--
55