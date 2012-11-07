--TEST--
This test has php 5.5 behaviour in mind:
empty can work on results of expressions

--COMPILEONLY--
--FILE--
<?php
$a = '';
$b = 0;
$c = 5;
echo empty($a) . "=\n";
echo empty($b) . "=\n";
echo empty($c) . "=\n";
echo empty(12 * 42) . "=\n";
echo empty(12 - 12) . "=\n";

?>
--EXPECT--
