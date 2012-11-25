--TEST--
Test in-place for reference
--FILE--
<?php
$a = 5;
$b = & $a;
$a += 10;
echo $b . "=\n";
echo $a . "=\n";
$c = & $b;
$b += 5;
echo $b . "=\n";
echo $c . "=\n";
echo $a . "=";
--EXPECT--
15=
15=
20=
20=
20=